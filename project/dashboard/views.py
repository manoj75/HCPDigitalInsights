import json
import requests
import adal
import re
import os
from project.models import User ,Profession,SpecialtyGroup,Segment,GeoRegions,Customer
from project.models import Campaign 
from flask import Blueprint,render_template, redirect,url_for,request,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

dashboard_blueprint =   Blueprint(
    'dashboard',
    __name__,
    template_folder='templates'
)


@dashboard_blueprint.route("/")
@login_required
def Index():
    campaigns   =   Campaign.query.filter_by(customerId=current_user.customerid)
    customerName=Customer.query.get(current_user.customerid).name
    return render_template('dashboard/index.html',customer_name=customerName,campaigns=campaigns)


@dashboard_blueprint.route("/campaign/<id>")
@login_required
def ShowCampaign(id):
    campaignId=id
    resource_url = 'https://analysis.windows.net/powerbi/api'
    #username='***'
    #password='***'
    PbiUserID       = str(os.environ['PbiUserID'])
    PbiPassword     = str(os.environ['PbiPassword'])
    
    print("-------------------------")
    
    print("PBIUserId="+PbiUserID)
    print("PbiPassword="+PbiPassword)
    print("-------------------------")
    print(current_user)
    #profession=Profession.query.all()
    client_id='4e4bf593-32b5-4d99-a860-bb26cdb0e2f7'
    AuthContext= adal.AuthenticationContext("https://login.windows.net/common")
    token=AuthContext.acquire_token_with_username_password(resource_url,PbiUserID,PbiPassword,client_id)
    accessToken=token["accessToken"]
    url="https://api.powerbi.com/v1.0/myorg/groups/42b9d168-fefb-4b3c-aa2d-af24fb08f4d8/reports"
    headers = {'Authorization': 'Bearer ' + accessToken,'Content-type': 'application/json', 'Accept': 'application/json'}
    response=requests.get(url, headers=headers)
    reportId=response.json()["value"][0]['id']
    reportUrl=response.json()["value"][0]["webUrl"]+"/GenerateToken"
    #reportUrl="https://api.powerbi.com/v1.0/myorg/reports/"+response.json()["value"][0]['id']+"/GenerateToken"
    reportId="f01e98f3-abb9-4f51-bca3-a9eb419ee97e"
    reportId="187ffc03-1c8e-4cb8-a19c-d182c2b01b16"
    reportUrl="https://api.powerbi.com/v1.0/myorg/groups/42b9d168-fefb-4b3c-aa2d-af24fb08f4d8/reports/"+reportId+"/GenerateToken"
    data1= {
            'allowSaveAs'   : 'false',
            "accessLevel"   : "view",
            "identities"    : [
                                {
                                    "username":campaignId,
                                    "roles":["Campaign"],
                                    "datasets":["80529fbe-4cae-49aa-a27c-2106c3d8aad7"]
                                }
                              ]
            }

    responseEmbedToken=requests.post(reportUrl,data=json.dumps(data1),headers=headers)
    embedurl="https://app.powerbi.com/reportEmbed?reportId="+reportId+"&groupId=42b9d168-fefb-4b3c-aa2d-af24fb08f4d8"
    configObj={'token':responseEmbedToken.json()["token"],'embedurl':embedurl,'reportid':reportId}
    professions=Profession.query.all()
    specialtyGroups=SpecialtyGroup.query.all()
    geoRegions=GeoRegions.query.all()
    Segments=Segment.query.all()
    customerName=Customer.query.get(current_user.customerid).name

    return render_template('dashboard/Pbi.html',customer_name=customerName,segments=Segments,professions=professions,specialtyGroups=specialtyGroups,geoRegions=geoRegions,configObj=json.dumps(configObj))


@dashboard_blueprint.route("/ProfessionalInsights")
@login_required
def ProfessionalInsights():
    return render_template('dashboard/index.html')

@dashboard_blueprint.route("/ContentInsights")
@login_required
def ContentInsights():
    return render_template('dashboard/ContentInsights.html')


@dashboard_blueprint.route("/DeviceTypes")
@login_required
def DeviceTypes():
    return render_template('dashboard/DeviceType.html')
