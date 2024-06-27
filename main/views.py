from django.shortcuts import render, redirect
from urllib.request import urlopen
from json import loads
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import User
from django.http import Http404
import base64, scratchattach

def baserender(request, template, context = {}):
    context["user"] = request.user
    context["logged_in"] = not request.user.get_username() == ""
    context["succeedmessage"] = request.GET.get("succeed")
    context["errormessage"] = request.GET.get("error")
    context["infomessage"] = request.GET.get("info")
    return render(request, template, context)

def indexView(request):
    featured = loads(urlopen("https://api.scratch.mit.edu/proxy/featured").read())
    return baserender(request, "index.html", {"featured": featured})

def choose_account_option(request):
    if request.GET.get("mode") == "SA":
        encoded = str(base64.b64encode(f'http://127.0.0.1:8000/verifylogin/?type={request.GET.get("type")}&mode=SA'.encode('ascii')))
        encoded_list = []
        for i in encoded:
            encoded_list.append(str(i))
        encoded_list.pop(0)
        encoded_list.pop(0)
        encoded_list.pop(len(encoded_list) - 1)
        encoded = ""
        for i in encoded_list:
            encoded = encoded + i
        return redirect(f"https://auth.itinerary.eu.org/auth/?redirect={encoded}&name=Switch")
    elif request.GET.get("mode") == "PA": return baserender(request, "login.html", {"type": request.GET.get("type")})
    else:
        return baserender(request, "choose_account.html", {"type": request.GET.get("type"), "auth_link": f"/login/?type={request.GET.get('type')}&mode=SA", "pass_link": f"/login/?type={request.GET.get('type')}&mode=PA"})

def VerifyLogin(request):
        if request.GET.get("mode") == "SA":
            response = urlopen("https://auth.itinerary.eu.org/api/auth/verifyToken?privateCode=" + request.GET.get("privateCode"))
            json_response = loads(response.read())
            if json_response["valid"] == True:
                if request.GET.get("type") == "login":
                    login(request, authenticate(request, username=json_response["username"], password="GeneratedScratchAccount"))
                    return redirect("/?succeed=Successfully logged in!")
                else:
                    try: 
                        User.objects.get(username=json_response["username"])
                        return redirect("/?error=You already have an account! Please choose 'login' instead.")
                    except:
                        pass
                    new_user = User.objects.create_user(username=json_response["username"], password="GeneratedScratchAccount")
                    login(request, new_user)
                    return redirect("/?succeed=Successfully linked account!")
            else:
                return redirect("/?error=An error occured")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            if request.GET.get("type") == "login":
                try:
                    user = authenticate(request, username=username, password=password)
                    if user.account_type == "PA":
                        login(request, user)
                    else:
                        raise
                except:
                    return redirect("/login/?error=Username/Password incorrect.&mode=PA&type=login")
                return redirect("/?succeed=Successfully logged in!")
            else:
                try: User.objects.get(username=username); return redirect("/?error=You already have an account! Please choose 'login' instead.")
                except: pass
                try: scratchattach.login(username, password)
                except: return redirect("/login/?error=Username/Password incorrect.&mode=PA&type=create")
                new_user = User.objects.create_user(username=username, password=password)
                login(request, new_user)
                return redirect("/?succeed=Successfully linked account!")


def Logout(request):
    logout(request)
    return redirect(reverse("index") + "?succeed=Successfully logged out!")

def projectView(request, project_id):
    project = scratchattach.get_project(project_id)
    if project.is_shared():
        return baserender(request, "project.html", {"project": project})
    else:
        raise Http404()