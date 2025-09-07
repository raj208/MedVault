from django.contrib.auth import get_user_model
from myapp.models import Doctor

User = get_user_model()

seed = [
    {
        "username": "dr_arjun_mehta", "email": "arjun.mehta@example.com", "password": "Password123!",
        "doctor": {
            "name": "Arjun Mehta",
            "specialties": ["Cardiology", "Internal Medicine"],
            "years_of_experience": 16,
            "hospital": "Bombay Heart Institute",
            "about": "Cardiologist with focus on ischemic heart disease and preventive cardiology.",
            "treatments": ["ECG", "Echocardiography", "Hypertension management", "Cholesterol management"],
            "city": "Mumbai", "pincode": "400001",
            "languages": ["en", "hi", "mr"],
            "phone": "+91 90000 10001", "email": "arjun.mehta@example.com",
            "license_number": "MH-2020-0001", "is_active": True
        }
    },
    {
        "username": "dr_neha_rao", "email": "neha.rao@example.com", "password": "Password123!",
        "doctor": {
            "name": "Neha Rao",
            "specialties": ["Cardiology", "Interventional Cardiology"],
            "years_of_experience": 12,
            "hospital": "Bengaluru Cardiac Care",
            "about": "Interventional cardiologist performing angioplasty and stenting.",
            "treatments": ["Angioplasty", "Stent placement", "Stress test"],
            "city": "Bengaluru", "pincode": "560001",
            "languages": ["en", "kn", "hi"],
            "phone": "+91 90000 10002", "email": "neha.rao@example.com",
            "license_number": "KA-2015-0456", "is_active": True
        }
    },
    {
        "username": "dr_saira_khan", "email": "saira.khan@example.com", "password": "Password123!",
        "doctor": {
            "name": "Saira Khan",
            "specialties": ["Gastroenterology"],
            "years_of_experience": 14,
            "hospital": "New Delhi Digestive Center",
            "about": "Expert in hepatology and inflammatory bowel disease.",
            "treatments": ["Endoscopy", "Colonoscopy", "Liver disease management"],
            "city": "New Delhi", "pincode": "110001",
            "languages": ["en", "hi"],
            "phone": "+91 90000 10003", "email": "saira.khan@example.com",
            "license_number": "DL-2012-0789", "is_active": True
        }
    },
    {
        "username": "dr_v_srinivasan", "email": "v.srinivasan@example.com", "password": "Password123!",
        "doctor": {
            "name": "V. Srinivasan",
            "specialties": ["Pulmonology", "Internal Medicine"],
            "years_of_experience": 18,
            "hospital": "Chennai Lung & Sleep Clinic",
            "about": "Pulmonologist with focus on COPD, asthma, and sleep apnea.",
            "treatments": ["Pulmonary function test", "Sleep study", "Asthma management"],
            "city": "Chennai", "pincode": "600001",
            "languages": ["en", "ta"],
            "phone": "+91 90000 10004", "email": "v.srinivasan@example.com",
            "license_number": "TN-2008-1122", "is_active": True
        }
    },
    {
        "username": "dr_priya_desai", "email": "priya.desai@example.com", "password": "Password123!",
        "doctor": {
            "name": "Priya Desai",
            "specialties": ["Endocrinology", "Internal Medicine"],
            "years_of_experience": 10,
            "hospital": "Ahmedabad Endocrine & Diabetes Center",
            "about": "Treats diabetes, thyroid, and metabolic disorders.",
            "treatments": ["Diabetes management", "Thyroid ultrasound", "PCOS management"],
            "city": "Ahmedabad", "pincode": "380001",
            "languages": ["en", "gu", "hi"],
            "phone": "+91 90000 10005", "email": "priya.desai@example.com",
            "license_number": "GJ-2017-3344", "is_active": True
        }
    },
    {
        "username": "dr_rakesh_gupta", "email": "rakesh.gupta@example.com", "password": "Password123!",
        "doctor": {
            "name": "Rakesh Gupta",
            "specialties": ["Orthopedics"],
            "years_of_experience": 20,
            "hospital": "Kolkata Ortho & Sports Medicine",
            "about": "Orthopedic surgeon for joint replacements and sports injuries.",
            "treatments": ["Knee replacement", "Arthroscopy", "Fracture fixation"],
            "city": "Kolkata", "pincode": "700001",
            "languages": ["en", "hi", "bn"],
            "phone": "+91 90000 10006", "email": "rakesh.gupta@example.com",
            "license_number": "WB-2005-5566", "is_active": True
        }
    },
    {
        "username": "dr_maria_dsouza", "email": "maria.dsouza@example.com", "password": "Password123!",
        "doctor": {
            "name": "Maria D'Souza",
            "specialties": ["Obstetrics & Gynecology"],
            "years_of_experience": 13,
            "hospital": "Mumbai Women’s Health Center",
            "about": "OB/GYN with focus on high-risk pregnancies and minimally invasive surgery.",
            "treatments": ["Antenatal care", "Laparoscopy", "Infertility evaluation"],
            "city": "Mumbai", "pincode": "400001",
            "languages": ["en", "mr"],
            "phone": "+91 90000 10007", "email": "maria.dsouza@example.com",
            "license_number": "MH-2011-7788", "is_active": True
        }
    },
    {
        "username": "dr_anil_kumar", "email": "anil.kumar@example.com", "password": "Password123!",
        "doctor": {
            "name": "Anil Kumar",
            "specialties": ["Pediatrics"],
            "years_of_experience": 9,
            "hospital": "Hyderabad Child Care",
            "about": "General pediatrics and vaccinations; adolescent health.",
            "treatments": ["Immunization", "Growth assessment", "Asthma in children"],
            "city": "Hyderabad", "pincode": "500001",
            "languages": ["en", "te", "hi"],
            "phone": "+91 90000 10008", "email": "anil.kumar@example.com",
            "license_number": "TS-2019-9911", "is_active": True
        }
    },
    {
        "username": "dr_kavita_sharma", "email": "kavita.sharma@example.com", "password": "Password123!",
        "doctor": {
            "name": "Kavita Sharma",
            "specialties": ["Nephrology", "Internal Medicine"],
            "years_of_experience": 11,
            "hospital": "Pune Kidney & Hypertension Clinic",
            "about": "Manages chronic kidney disease and dialysis patients.",
            "treatments": ["Dialysis", "Kidney biopsy", "Hypertension control"],
            "city": "Pune", "pincode": "411001",
            "languages": ["en", "hi", "mr"],
            "phone": "+91 90000 10009", "email": "kavita.sharma@example.com",
            "license_number": "MH-2016-2222", "is_active": True
        }
    },
    {
        "username": "dr_rohit_banerjee", "email": "rohit.banerjee@example.com", "password": "Password123!",
        "doctor": {
            "name": "Rohit Banerjee",
            "specialties": ["Cardiology", "Electrophysiology"],
            "years_of_experience": 8,
            "hospital": "Kolkata Heart Rhythm Center",
            "about": "Cardiac electrophysiologist focusing on arrhythmias.",
            "treatments": ["Holter monitoring", "Pacemaker/ICD follow-up", "Ablation referral"],
            "city": "Kolkata", "pincode": "700001",
            "languages": ["en", "bn"],
            "phone": "+91 90000 10010", "email": "rohit.banerjee@example.com",
            "license_number": "WB-2018-1234", "is_active": True
        }
    },
]

created, updated = 0, 0
for row in seed:
    # create or update auth user
    user, _ = User.objects.get_or_create(username=row["username"], defaults={"email": row["email"]})
    if not user.has_usable_password():
        user.set_password(row["password"])
        user.email = row["email"]
        user.save()

    d = row["doctor"]
    # upsert Doctor linked to this user (OneToOne primary key)
    obj, was_created = Doctor.objects.update_or_create(
        user=user,
        defaults={
            "name": d["name"],
            "specialties": d["specialties"],
            "years_of_experience": d["years_of_experience"],
            "hospital": d["hospital"],
            "about": d["about"],
            "treatments": d["treatments"],
            "city": d["city"],
            "pincode": d["pincode"],
            "languages": d["languages"],
            "phone": d["phone"],
            "email": d["email"],
            "license_number": d["license_number"],
            "is_active": d["is_active"],
        },
    )
    created += int(was_created)
    updated += int(not was_created)

print(f"Doctors created: {created}, updated: {updated}")
