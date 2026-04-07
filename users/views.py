from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

from users.forms import UserRegistrationForm
from .models import UserRegistrationModel
import re

def is_gibberish(text):
    """
    Heuristic to detect keyboard mashing (gibberish).
    """
    if not text or len(text.strip()) < 3:
        return True
    
    words = text.split()
    for word in words:
        # Check if a single word is too long without any common vowel (keyboard mashing)
        if len(word) > 8:
            vowels = len(re.findall(r'[aeiouy]', word, re.IGNORECASE))
            if vowels / len(word) < 0.25: # Stricter vowel ratio for long words
                return True
        
        # Check for long consonant runs (more than 4)
        if re.search(r'[^aeiouy\s\d]{5,}', word, re.IGNORECASE):
            return True
            
    return False


# ---------------- USER REGISTRATION ----------------

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegister.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'UserRegister.html', {'form': form})


# ---------------- USER LOGIN ----------------

def UserLoginCheck(request):
    if request.method == "POST":

        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')

        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)

            if check.status == "activated":

                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email

                return render(request, 'users/UserHomePage.html', {})

            else:
                messages.error(request, 'Your Account Not Activated')
                return render(request, 'UserLogin.html')

        except:
            messages.error(request, 'Invalid Login id and password')

    return render(request, 'UserLogin.html')


# ---------------- USER HOME ----------------

def UserHome(request):
    return render(request, 'users/UserHomePage.html')


# ---------------- TEXT TO IMAGE GENERATION ----------------

def test_text_to_image(request):

    if request.method != "POST":
        return render(request, "users/test_form.html")

    prompt = request.POST.get("prompt", "").strip()

    if not prompt or is_gibberish(prompt):
        messages.error(request, "Invalid Text: Please enter a meaningful prompt for better results.")
        return render(request, "users/test_form.html")

    try:
        import requests as req
        from PIL import Image
        import io
        import urllib.parse

        # Get chosen provider from form, default to 'pollinations' as it is more reliable (free)
        provider = request.POST.get("provider", "pollinations")

        if provider == "pollinations":
            # --- Pollinations.ai (Free, No Token Required) ---
            encoded_prompt = urllib.parse.quote(prompt)
            API_URL = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true"
            
            print(f"DEBUG: Sending request to Pollinations.ai with prompt: {prompt}")
            response = req.get(API_URL)
            provider_name = "Pollinations.ai (Free)"
        
        else:
            # --- Hugging Face Inference API ---
            # HF Token should be set in environment variables
            HF_TOKEN = os.environ.get("HF_TOKEN", "")
            
            if HF_TOKEN:
                print(f"DEBUG: Using Hugging Face Token: {HF_TOKEN[:5]}...{HF_TOKEN[-5:]}")
            else:
                print("DEBUG: Using Hugging Face without Token (Public)")
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            payload = {"inputs": prompt}

            print(f"DEBUG: Sending request to {API_URL} with prompt: {prompt}")
            response = req.post(API_URL, headers=headers, json=payload)
            provider_name = "Hugging Face Inference API"

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            
            # Sanitize filename (remove special chars)
            clean_prompt = "".join(x for x in prompt[:20] if x.isalnum() or x in "._- ").strip().replace(' ', '_')
            filename = f"generated_{clean_prompt}_{os.urandom(4).hex()}.png"
            
            save_path = os.path.join(settings.MEDIA_ROOT, filename)
            image.save(save_path)

            return render(
                request,
                "users/test_form_result.html",
                {
                    "image_url": settings.MEDIA_URL + filename,
                    "prompt": prompt,
                    "provider": provider_name
                }
            )
        else:
            return HttpResponse(f"<h3>Image Generation Error</h3><p>Status: {response.status_code}</p><p>Response: {response.text}</p><p><a href='/test_text_to_image/'>Go Back</a></p>")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

 

 