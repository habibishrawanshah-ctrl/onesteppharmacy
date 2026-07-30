from django.core.management.base import BaseCommand
from products.models import Product, Category


CATEGORY_MAP = {
    'pain-relief': 'Pain Relief',
    'cold-cough': 'Cold & Cough',
    'stomach-care': 'Stomach Care',
    'vitamins-minerals': 'Vitamins & Minerals',
    'diabetic-care': 'Diabetic Care',
    'cardiac-care': 'Cardiac Care',
    'wound-care': 'Wound Care',
    'skin-care': 'Skin Care',
    'allergy-fever': 'Allergy & Fever',
    'baby-care': 'Baby Care',
    'eye-ear-care': 'Eye & Ear Care',
    'bone-joint': 'Bone, Joint & Muscle',
    'respiratory': 'Respiratory Care',
    'liver-care': 'Liver Care',
    'sexual-wellness': 'Sexual Wellness',
    'first-aid': 'First Aid',
}


PRODUCT_BY_CATEGORY = {

    'pain-relief': [
        ("Amrutanjan Headache Faster Relaxation Roll-on 10ml", 75, "Fast relief roll-on for headaches and body pain", 100, False),
        ("Dr.Ortho Oil 120ml", 276, "Ayurvedic oil for joint and muscle pain relief", 80, False),
        ("Volini Pain Relief Spray 100g", 285, "Topical pain relief spray for sprains and muscle pain", 90, False),
        ("Moov Pain Relief Spray 100ml", 245, "Fast acting pain relief spray for back and joint pain", 85, False),
        ("Iodex Pain Balm 25g", 95, "Warming balm for muscular pain and stiffness", 120, False),
        ("Omnigel Diclofenac Gel 30g", 145, "Anti-inflammatory gel for localized pain relief", 95, False),
        ("Combiflam Tablets 15s", 55, "Ibuprofen + Paracetamol for pain and fever", 150, False),
        ("Dolo 650 Tablets 15s", 75, "Paracetamol 650mg for fever and body pain", 200, False),
        ("Crocin Advance Tablets 10s", 35, "Paracetamol 500mg for mild to moderate pain", 250, False),
        ("Voveron SR 100mg Tablets 10s", 65, "Diclofenac sodium for joint and muscle pain", 100, False),
        ("Nise 100mg Tablets 10s", 70, "Nimesulide 100mg for acute pain relief", 90, False),
        ("Skelactin 500mg Tablets 10s", 90, "Chlorzoxazone for muscle spasms and pain", 70, False),
        ("Flexon MR Tablets 10s", 85, "Diclofenac + Paracetamol + Chlorzoxazone for muscle pain", 80, False),
        ("Sumo Tablets 10s", 60, "Paracetamol + Caffeine for headache relief", 180, False),
        ("Saridon Tablets 10s", 40, "Paracetamol + Caffeine + Propyphenazone for headaches", 200, False),
        ("Zerodol SP Tablets 10s", 95, "Aceclofenac + Paracetamol + Serratiopeptidase for inflammation", 75, False),
        ("Mobizox MR Tablets 10s", 80, "Etoricoxib + Chlorzoxazone for musculoskeletal pain", 60, False),
        ("Volini Pain Relief Gel 30g", 165, "Topical analgesic gel for localized pain", 100, False),
        ("Rablet Thermol Collar", 299, "Self-heating neck wrap for cervical pain relief", 40, False),
        ("Tiger Balm Red 19g", 120, "Traditional medicated ointment for aches and pains", 110, False),
        ("Zandu Balm 25ml", 55, "Ayurvedic balm for headache and body pain", 150, False),
    ],

    'cold-cough': [
        ("Benadryl Cough Syrup 100ml", 85, "Diphenhydramine cough suppressant syrup", 120, False),
        ("Alex Cough Syrup 100ml", 95, "Expectorant for productive cough relief", 110, False),
        ("Corex Cough Syrup 100ml", 110, "Codeine-based cough syrup for dry cough", 90, True),
        ("Ascoril LS Syrup 100ml", 125, "Expectorant + bronchodilator for chest congestion", 100, False),
        ("Sinarest Nasal Spray 10ml", 120, "Nasal decongestant spray for cold relief", 80, False),
        ("Vicks VapoRub 25g", 85, "Topical ointment for cold and congestion relief", 200, False),
        ("Dabur Tulsi Drops 15ml", 65, "Ayurvedic drops for cold, cough and immunity", 150, False),
        ("Koflet Lozenges Pack 12s", 35, "Herbal lozenges for sore throat relief", 200, False),
        ("Chericof Syrup 100ml", 90, "Cough formula for dry and productive cough", 100, False),
        ("Delcof Capsules 10s", 75, "Noscapine + Chlorpheniramine for cough", 80, False),
        ("Solvin Expectorant 100ml", 80, "Ambroxol + Terbutaline + Guaifenesin for chest congestion", 100, False),
        ("Mucolite Syrup 100ml", 70, "Acetylcysteine mucolytic for thick phlegm", 90, False),
        ("Phensedyl Cough Linctus 100ml", 120, "Codeine-based linctus for dry irritating cough", 70, True),
        ("Honitus Syrup 100ml", 85, "Ayurvedic cough syrup for cold and cough", 120, False),
        ("Halls Menthol Cough Drops 30g", 30, "Menthol cough drops for temporary throat relief", 250, False),
        ("Strepsils Lozenges Pack 24s", 95, "Antibacterial lozenges for sore throat", 180, False),
        ("Coldact Capsules 10s", 55, "Chlorpheniramine + Phenylpropanolamine for cold", 150, False),
        ("Cetzine 10mg Tablets 10s", 40, "Cetirizine for allergy and cold symptoms", 200, False),
    ],

    'stomach-care': [
        ("Digene Gel 100ml", 85, "Antacid for acidity and heartburn relief", 120, False),
        ("Gelusil MPS Suspension 100ml", 80, "Antacid + Simethicone for gas and acidity", 100, False),
        ("Pantop 40mg Tablets 10s", 65, "Pantoprazole for acid reflux and GERD", 150, False),
        ("Rantac 150mg Tablets 10s", 35, "Ranitidine for stomach ulcers and acidity", 200, False),
        ("Cyra D Capsules 10s", 85, "Pantoprazole + Domperidone for reflux", 100, False),
        ("Omez Capsules 20mg 10s", 55, "Omeprazole for acid peptic disorders", 180, False),
        ("Eno Fruit Salt Lemon 60g", 45, "Instant antacid powder for acidity relief", 250, False),
        ("Cremaffin Plus Suspension 170ml", 95, "Milk of magnesia + liquid paraffin for constipation", 80, False),
        ("PEG Aspar Powder 10s", 120, "Polyethylene glycol for constipation relief", 60, False),
        ("Enterogermina Probiotic 6s", 95, "Probiotic spore suspension for gut health", 100, False),
        ("Econorm Probiotic Capsules 10s", 110, "Probiotic for diarrhea and digestive health", 90, False),
        ("Lomotil Tablets 10s", 50, "Diphenoxylate + Atropine for diarrhea", 80, True),
        ("ORS Powder Lemon 21.8g Pack 5s", 30, "Oral rehydration salts for dehydration", 300, False),
        ("Colospa Retard Tablets 10s", 90, "Mebeverine for irritable bowel syndrome", 70, False),
        ("Pudin Hara Pearls 10s", 55, "Ayurvedic digestive pearls for gas and bloating", 150, False),
        ("Zintac 150mg Tablets 10s", 40, "Ranitidine for acidity and heartburn", 200, False),
        ("Rantac DSR Capsules 10s", 75, "Domperidone + Ranitidine for reflux", 120, False),
        ("Meftal Spas Tablets 10s", 60, "Mefenamic acid + Dicyclomine for abdominal cramps", 100, False),
    ],

    'vitamins-minerals': [
        ("Supa Radiance Multivitamin Tablets 30s", 180, "Complete multivitamin for daily wellness", 100, False),
        ("Zincovit Tablets 15s", 75, "Multivitamin with zinc for immunity", 200, False),
        ("Becosules Capsules 30s", 120, "B-complex vitamins for energy metabolism", 150, False),
        ("Neurobion Forte Tablets 30s", 95, "Vitamin B-complex for nerve health", 120, False),
        ("A to Z Multivitamin Tablets 30s", 145, "Comprehensive multivitamin with minerals", 130, False),
        ("Calcium Sandoz 500mg Tablets 30s", 110, "Calcium supplement for bone health", 140, False),
        ("Calcimax Forte Tablets 30s", 165, "Calcium + Vitamin D3 + Magnesium for bones", 100, False),
        ("Shelcal 500mg Tablets 30s", 130, "Calcium carbonate for bone strength", 120, False),
        ("Ferradol Capsules 30s", 155, "Iron + Folic acid + B12 for anemia", 90, False),
        ("D3 60K Capsules 4s", 85, "Vitamin D3 60000IU weekly supplement", 180, False),
        ("Ostogen D3 60K Capsules 4s", 80, "Vitamin D3 for bone and immune health", 150, False),
        ("Limcee 500mg Tablets 15s", 45, "Vitamin C chewable for immunity", 250, False),
        ("Celin 500mg Tablets 15s", 40, "Vitamin C tablets for antioxidant support", 200, False),
        ("Becadexamin Capsules 30s", 90, "Multivitamin with minerals for overall health", 100, False),
        ("Revital H Capsules 30s", 195, "Multivitamin with ginseng and minerals", 110, False),
        ("Macroberin Plus Tablets 30s", 140, "Vitamin B-complex with antioxidants", 80, False),
        ("Folvite 5mg Tablets 30s", 35, "Folic acid supplement for pregnancy", 120, False),
        ("Omega-3 Fish Oil Softgels 30s", 220, "Omega-3 fatty acids for heart and brain health", 90, False),
        ("Seven Seas Cod Liver Oil Capsules 30s", 165, "Cod liver oil with Vitamins A and D", 85, False),
    ],

    'diabetic-care': [
        ("Gluconorm SR 500mg Tablets 10s", 45, "Metformin SR for type 2 diabetes", 200, True),
        ("Gluconorm PG 2mg/500mg Tablets 10s", 55, "Glimepiride + Metformin combination", 150, True),
        ("Januvia 100mg Tablets 14s", 450, "Sitagliptin for type 2 diabetes", 50, True),
        ("Galvus Met 50mg/500mg Tablets 15s", 120, "Vildagliptin + Metformin for diabetes", 80, True),
        ("Glimestar 1mg Tablets 10s", 35, "Glimepiride for blood sugar control", 180, True),
        ("Pioglit 15mg Tablets 10s", 40, "Pioglitazone for insulin sensitivity", 100, True),
        ("Diapride M Tablets 15s", 65, "Gliclazide + Metformin for diabetes", 120, True),
        ("Gluconorm 500mg Tablets 20s", 55, "Metformin 500mg for blood glucose control", 250, True),
        ("Insulin Syringes U-100 1ml Pack 10s", 120, "Disposable insulin syringes with needle", 200, True),
        ("Accu-Chek Instant Test Strips 50s", 981, "Blood glucose test strips for Accu-Chek meters", 150, False),
        ("OneTouch Ultra Test Strips 50s", 1139, "Blood glucose test strips for OneTouch meters", 100, False),
        ("Dr.Morepen Glucometer Test Strips 50s", 596, "Blood glucose test strips for BG-03 meter", 180, False),
        ("Sugar-Free Green Powder 100g", 195, "Low-calorie sweetener for diabetic diet", 120, False),
        ("Diabeto Capsules 60s", 240, "Ayurvedic supplement for sugar management", 60, False),
        ("Karela Jamun Juice 1L", 180, "Bitter gourd and jamun juice for diabetes", 80, False),
        ("Diabetic Multivitamin Tablets 30s", 220, "Multivitamin formulated for diabetics", 70, False),
    ],

    'cardiac-care': [
        ("Amlodac 5mg Tablets 10s", 35, "Amlodipine for hypertension and angina", 200, True),
        ("Storvas 10mg Tablets 10s", 55, "Atorvastatin for cholesterol management", 180, True),
        ("Ecosprin 75mg Tablets 14s", 25, "Aspirin 75mg for blood thinning", 300, True),
        ("Sarpagandha Tablets 60s", 120, "Ayurvedic herb for blood pressure support", 80, False),
        ("Candesar 8mg Tablets 10s", 55, "Candesartan for hypertension", 100, True),
        ("Lozart 50mg Tablets 10s", 45, "Losartan potassium for blood pressure", 150, True),
        ("Nebistar 2.5mg Tablets 10s", 65, "Nebivolol for hypertension", 90, True),
        ("Met XL 25mg Tablets 10s", 40, "Metoprolol succinate for heart conditions", 120, True),
        ("Rostil 10mg Tablets 10s", 75, "Rosuvastatin for cholesterol control", 140, True),
        ("Atheroze 20mg Tablets 10s", 85, "Atorvastatin + Ezetimibe for lipid control", 80, True),
        ("Clopilet 75mg Tablets 10s", 55, "Clopidogrel for heart attack prevention", 100, True),
        ("Cardivas 3.125mg Tablets 10s", 70, "Carvedilol for heart failure management", 70, True),
        ("Telmikind 40mg Tablets 10s", 50, "Telmisartan for hypertension management", 130, True),
        ("Ramistar 5mg Tablets 10s", 60, "Ramipril for hypertension and heart health", 110, True),
        ("Omega 3 Heart Capsules 60s", 295, "Omega 3 fatty acids for cardiovascular support", 90, False),
    ],

    'wound-care': [
        ("Band-Aid Surgical Plaster 20s", 40, "Adhesive bandages for minor cuts and wounds", 300, False),
        ("Dettol Antiseptic Liquid 500ml", 195, "Antiseptic liquid for wound cleaning", 150, False),
        ("Savlon Antiseptic Liquid 500ml", 165, "Antiseptic disinfectant for wounds", 140, False),
        ("Soframycin Skin Cream 15g", 60, "Framycetin antibiotic cream for wounds", 120, False),
        ("Neosporin Ointment 15g", 55, "Neomycin + Bacitracin antibiotic ointment", 180, False),
        ("Betadine Antiseptic Ointment 10g", 40, "Povidone-iodine ointment for wound disinfection", 200, False),
        ("Dettol Antiseptic Cream 30g", 75, "Antiseptic cream for cuts and grazes", 100, False),
        ("Hydrogen Peroxide 100ml", 35, "Antiseptic solution for wound cleaning", 200, False),
        ("Sterile Gauze Swabs Pack 10s", 45, "Sterile cotton gauze for wound dressing", 250, False),
        ("Crepe Bandage 4 Inch 4.5m", 55, "Elastic crepe bandage for sprains and support", 180, False),
        ("Surgical Adhesive Tape 2.5cm x 5m", 35, "Medical tape for securing dressings", 200, False),
        ("Cotton Wool Roll 100g", 45, "Absorbent cotton wool for medical use", 200, False),
        ("Burnol Burn Cream 30g", 85, "Burn relief cream for minor burns and scalds", 80, False),
        ("Flexicare Wound Dressing 10x10cm", 65, "Non-stick wound dressing pad", 100, False),
        ("Metrogyl Gel 30g", 55, "Metronidazole gel for wound healing", 90, False),
    ],

    'skin-care': [
        ("Cetaphil Gentle Skin Cleanser 250ml", 420, "Gentle cleansing lotion for sensitive skin", 80, False),
        ("Nivea Moisturising Cream 200ml", 195, "Daily moisturizing cream for all skin types", 150, False),
        ("Sunscoop Sunscreen SPF 50 PA+++ 50g", 295, "Broad-spectrum sunscreen for sun protection", 100, False),
        ("Boroplus Antiseptic Cream 50g", 80, "Multi-purpose Ayurvedic cream for skin", 200, False),
        ("Ponds Cold Cream 100g", 95, "Moisturizing cream for dry skin", 150, False),
        ("Clobetamethasone Cream 15g", 90, "Clobetasol propionate for skin conditions", 100, True),
        ("Candid Cream 15g", 60, "Clotrimazole antifungal cream for skin infections", 120, False),
        ("Clocip Cream 15g", 55, "Clobetasol + Ofloxacin + Miconazole for skin issues", 100, True),
        ("Fungiderm Cream 15g", 50, "Miconazole antifungal cream", 130, False),
        ("Adelphane Clean+ 100ml", 345, "Acne treatment face wash", 80, False),
        ("Sebamed Face Wash 100ml", 295, "pH-balanced face wash for sensitive skin", 70, False),
        ("Ecziderm Cream 30g", 120, "Treatment cream for eczema and dermatitis", 60, True),
        ("Aloe Vera Gel 100ml", 125, "Natural aloe vera gel for skin soothing", 100, False),
        ("Vicco Turmeric Cream 30g", 65, "Turmeric-based Ayurvedic skin cream", 180, False),
    ],

    'allergy-fever': [
        ("Cetzine 10mg Tablets 10s", 40, "Cetirizine for allergy symptoms", 250, False),
        ("Allegra 120mg Tablets 10s", 95, "Fexofenadine 120mg for seasonal allergies", 150, False),
        ("Levocet M Tablets 10s", 55, "Levocetirizine + Montelukast for allergy", 180, False),
        ("Montair 10mg Tablets 10s", 75, "Montelukast for allergy and asthma control", 160, False),
        ("Avil 25mg Tablets 10s", 30, "Pheniramine maleate for allergy skin reactions", 200, False),
        ("Dolo 650mg Tablets 15s", 75, "Paracetamol for fever and body pain", 250, False),
        ("Meftal P 500mg Tablets 10s", 50, "Mefenamic acid for fever and inflammation", 180, False),
        ("Nicip Plus Tablets 10s", 55, "Nimesulide + Paracetamol for fever", 150, False),
        ("Crocin 650mg Tablets 15s", 70, "Paracetamol 650mg for fever relief", 220, False),
        ("Calpol 500mg Tablets 15s", 55, "Paracetamol 500mg for children's fever", 200, False),
        ("Summeril 10mg Tablets 10s", 45, "Loratadine for antihistamine relief", 150, False),
        ("Histafree 5mg Tablets 10s", 35, "Levocetirizine for allergy symptoms", 180, False),
    ],

    'baby-care': [
        ("Pampers Premium Pants L Size 42s", 899, "Premium diaper pants for active babies", 80, False),
        ("Huggies Complete Comfort M Size 46s", 799, "Complete comfort diapers for medium babies", 70, False),
        ("MamyPoko Extra Dry L Size 42s", 749, "Extra dry diaper pants for long hours", 75, False),
        ("Johnson's Baby Powder 200g", 195, "Baby powder for gentle skin care", 150, False),
        ("Johnson's Baby Shampoo 200ml", 220, "Gentle tear-free baby shampoo", 120, False),
        ("Johnson's Baby Lotion 200ml", 245, "Moisturizing lotion for baby's delicate skin", 100, False),
        ("Johnson's Baby Oil 200ml", 210, "Gentle baby oil for massage and skin care", 130, False),
        ("Himalaya Baby Cream 100ml", 165, "Gentle baby cream for skin protection", 110, False),
        ("Mamaearth Baby Lotion 200ml", 299, "Natural baby lotion with shea butter", 90, False),
        ("Chicco Diaper Cream 50ml", 350, "Diaper rash cream for baby's sensitive skin", 60, False),
        ("Baby Wipes 72s Pack", 120, "Gentle baby wet wipes for cleaning", 200, False),
        ("Dabur Baby Massage Oil 200ml", 165, "Ayurvedic baby massage oil", 100, False),
        ("Cerecin Toothpaste 0-3 Years 40g", 120, "Fluoride-free toothpaste for toddlers", 80, False),
        ("Nestle Cerelac Wheat 300g", 195, "Infant cereal with milk for 6+ months", 100, False),
    ],

    'eye-ear-care': [
        ("Moisture Drops Eye Drops 10ml", 135, "Lubricating eye drops for dry eyes", 100, False),
        ("Refresh Tears Eye Drops 10ml", 150, "Artificial tears for dry eye relief", 90, False),
        ("I-Tear 5ml Eye Drops", 85, "Carboxymethylcellulose eye drops", 110, False),
        ("Eldex Eye Drops 10ml", 95, "Antibacterial eye drops for infections", 100, True),
        ("Zoxan Eye Drops 5ml", 120, "Ofloxacin antibiotic eye drops", 80, True),
        ("Gatiflo Eye Drops 5ml", 110, "Gatifloxacin eye drops for eye infections", 75, True),
        ("Pataday Eye Drops 2.5ml", 185, "Olopatadine for allergic conjunctivitis", 60, True),
        ("Zymar Eye Drops 5ml", 140, "Gatifloxacin for bacterial eye infections", 65, True),
        ("Soframycin Eye Drops 5ml", 55, "Framycetin antibiotic eye drops", 100, False),
        ("Earex Ear Drops 10ml", 85, "Olive oil ear drops for wax removal", 120, False),
        ("Waxsol Ear Drops 10ml", 95, "Docusate ear drops for ear wax softening", 100, False),
        ("Otoclear Ear Drops 10ml", 75, "Anti-infective ear drops for swimmer's ear", 80, True),
        ("Ciplox Ear Drops 10ml", 90, "Ciprofloxacin antibiotic ear drops", 70, True),
        ("Borosil Glass Eyewash Cup", 150, "Eyewash glass cup for eye cleaning", 50, False),
    ],

    'bone-joint': [
        ("Evion 400mg Capsules 30s", 110, "Vitamin E 400mg for joint and skin health", 100, False),
        ("Glucosamine Chondroitin Capsules 60s", 350, "Joint supplement for cartilage support", 80, False),
        ("Hepasule 500mg Capsules 60s", 295, "Glucosamine + Chondroitin + MSM for joints", 70, False),
        ("Sioril 100mg Tablets 10s", 85, "Nimesulide + Serratiopeptidase for inflammation", 100, False),
        ("Serratiopeptidase 10mg Tablets 10s", 65, "Enzyme supplement for inflammation reduction", 90, False),
        ("Calcimax Forte 30s", 165, "Calcium + Magnesium + Zinc + D3 for bones", 120, False),
        ("HP Gum Gum Forte Tablets 60s", 220, "Calcium + Vitamin D + K2 for bone density", 60, False),
        ("Rheumatol Capsules 60s", 180, "Herbal supplement for arthritis management", 50, False),
        ("Dr Ortho Ayurvedic Oil 120ml", 276, "Ayurvedic oil for joint and muscle relief", 80, False),
        ("Omron TENS Unit Pain Relief", 2499, "Electronic pain relief device for joints", 30, False),
        ("Knee Support Brace Adjustable", 350, "Adjustable knee cap for joint support", 60, False),
        ("Lumbar Support Belt Elastic", 450, "Elastic back support belt for lower back", 55, False),
    ],

    'respiratory': [
        ("Asthalin 100mcg Inhaler 200 doses", 195, "Salbutamol inhaler for asthma relief", 80, True),
        ("Fortipure Air Purifier Mask N95", 95, "N95 respirator mask for pollution protection", 200, False),
        ("Levolin 50mcg Rotacaps 30s", 85, "Levosalbutamol rotacaps for asthma", 70, True),
        ("Respules Budecort 0.5mg 5s", 165, "Budesonide nebulization suspension", 60, True),
        ("Foracort 200 Rotacaps 30s", 195, "Formoterol + Budesonide dry powder inhaler", 50, True),
        ("Deriphyllin Retard 300mg Tablets 10s", 50, "Etofylline bronchodilator for COPD", 90, True),
        ("Montek LC Tablets 10s", 85, "Montelukast + Levocetirizine for respiratory allergy", 120, False),
        ("Seroflo 250mcg Rotacaps 30s", 245, "Fluticasone + Salmeterol for asthma control", 40, True),
        ("Nebulizer Machine Compressor", 2800, "Compressor nebulizer for respiratory medication", 25, False),
        ("Steam Inhaler Vaporizer", 800, "Personal steam inhaler for congestion relief", 35, False),
        ("Peak Flow Meter", 450, "Handheld device for measuring lung function", 40, False),
        ("Breathe Right Nasal Strips 30s", 250, "Nasal dilator strips for easier breathing", 60, False),
    ],

    'liver-care': [
        ("Liv 52 Tablets 100s", 165, "Ayurvedic liver tonic for liver protection", 100, False),
        ("Livoluk Syrup 200ml", 150, "Liver tonic with herbal ingredients", 80, False),
        ("Silybon 70mg Tablets 60s", 195, "Silymarin 70mg for liver health", 70, False),
        ("Hepatogard Capsules 60s", 220, "Liver detox supplement with milk thistle", 60, False),
        ("Ursocol 300mg Tablets 10s", 145, "Ursodeoxycholic acid for liver conditions", 80, True),
        ("Rantac 150mg Tablets 10s", 35, "Ranitidine for gastric issues related to liver", 180, False),
        ("Cremaffin Plus 170ml", 95, "Laxative for constipation in liver patients", 90, False),
        ("Pan 40mg Tablets 10s", 65, "Pantoprazole for gastric protection", 150, False),
        ("LiverCare Capsules 60s", 250, "Herbal liver supplement with 9 Ayurvedic herbs", 50, False),
        ("Hepatamax Syrup 200ml", 165, "Liver tonic with L-ornithine L-aspartate", 60, False),
    ],

    'sexual-wellness': [
        ("Durex Extra Thin Condoms 10s", 220, "Ultra thin condoms for natural feel", 200, False),
        ("Durex Mutual Climax Condoms 12s", 350, "Condoms designed for mutual pleasure", 150, False),
        ("Durex Flavoured Condoms 10s", 250, "Assorted flavoured condoms", 180, False),
        ("Kama Sutra Condoms 12s", 180, "Premium condoms with ribbed texture", 200, False),
        ("Moods Condoms Ultra Thin 12s", 195, "Extra thin condoms for sensitive feel", 220, False),
        ("Prega News Pregnancy Test Kit 1pc", 60, "Home pregnancy test kit 99% accurate", 300, False),
        ("i-know Ovulation Test Strips 5s", 515, "Ovulation prediction test strips", 60, False),
        ("Apollo LH Ovulation 5 Day Test Kit", 421, "Ovulation test kit for fertility tracking", 80, False),
        ("Durex Lubricant Gel 50ml", 195, "Water-based personal lubricant gel", 120, False),
        ("KY Jelly Personal Lubricant 50ml", 250, "Medical-grade personal lubricant", 90, False),
        ("Sexual Wellness Herbal Capsules 60s", 350, "Natural supplement for libido support", 50, False),
        ("Manforce Condoms 12s", 140, "Dotted condoms for enhanced pleasure", 250, False),
        ("Condom Wallet Silver", 50, "Metal condom case keychain for 2 condoms", 100, False),
    ],

    'first-aid': [
        ("Dettol First Aid Kit 30pcs", 295, "Comprehensive first aid box for home", 80, False),
        ("Band-Aid Fabric Plaster 20s", 45, "Fabric bandages for flexible wound coverage", 250, False),
        ("Savlon Wound Wash 100ml", 135, "Sterile wound spray for cleaning injuries", 100, False),
        ("Instant Ice Pack 15x20cm", 85, "Instant cold pack for sprains and swelling", 60, False),
        ("Triangular Bandage 100x100cm", 45, "Cotton triangular bandage for arm sling", 100, False),
        ("Rescue Remedy Drops 10ml", 350, "Natural stress relief drops for emergencies", 40, False),
        ("CPR Mouth Barrier Shield", 120, "Disposable CPR face shield with valve", 50, False),
        ("Emergency Thermal Blanket", 95, "Compact emergency blanket for heat retention", 70, False),
        ("Whistle with Strap Emergency", 50, "Safety whistle for emergencies", 80, False),
        ("Multi-purpose First Aid Scissors", 65, "Stainless steel bandage scissors", 90, False),
        ("Disposable Latex Gloves Pack 10s", 75, "Powder-free latex examination gloves", 200, False),
        ("Cotton Buds Pack 100s", 35, "Sterile cotton buds for cleaning", 200, False),
        ("Tweezers Stainless Steel", 45, "Angled tweezers for splinter removal", 100, False),
        ("Hydrogel Burn Dressing 5x5cm", 95, "Hydrating burn dressing for cooling relief", 50, False),
    ],
}


class Command(BaseCommand):
    help = 'Seed database with comprehensive medicine products from Apollo Pharmacy catalogue'

    def add_arguments(self, parser):
        parser.add_argument('--categories', type=str, default='',
            help='Comma-separated list of category slugs to seed (default: all)')

    def handle(self, *args, **options):
        filter_cats = [c.strip() for c in options['categories'].split(',') if c.strip()]
        category_keys = filter_cats if filter_cats else list(PRODUCT_BY_CATEGORY.keys())

        total_imported = 0
        total_existing = 0

        for slug in category_keys:
            if slug not in CATEGORY_MAP:
                self.stdout.write(self.style.WARNING(f'Unknown category slug: {slug}, skipping'))
                continue

            cat_name = CATEGORY_MAP[slug]
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': cat_name},
            )
            if created:
                self.stdout.write(f'  Created category: {cat_name}')

            products = PRODUCT_BY_CATEGORY.get(slug, [])
            imported = 0
            existing = 0

            for name, price, desc, stock, rx in products:
                _, was_created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': cat,
                        'description': desc,
                        'price': price,
                        'stock': stock,
                        'is_prescription_required': rx,
                        'manufacturer': 'Apollo Pharmacy',
                    }
                )
                if was_created:
                    imported += 1
                else:
                    existing += 1

            self.stdout.write(f'  {cat_name}: {imported} new, {existing} existing')
            total_imported += imported
            total_existing += existing

        total = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Done. Imported {total_imported} new products. '
            f'Skipped {total_existing} existing. '
            f'Total in DB: {total}'
        ))
