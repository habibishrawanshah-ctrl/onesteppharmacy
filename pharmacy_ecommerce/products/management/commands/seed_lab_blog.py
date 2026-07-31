from django.core.management.base import BaseCommand
from django.utils.text import slugify
from lab.models import LabTest
from health.models import BlogPost


LAB_TESTS = [
    {
        'name': 'Complete Blood Count (CBC)',
        'description': 'Measures red blood cells, white blood cells, haemoglobin, platelets and other blood components to detect anaemia, infection and other disorders.',
        'price': 350,
        'category': 'blood',
        'preparation': 'No special preparation required. Fasting is not needed.',
    },
    {
        'name': 'Blood Sugar (Fasting)',
        'description': 'Measures glucose levels after 8-12 hours of fasting to screen for and monitor diabetes.',
        'price': 120,
        'category': 'blood',
        'preparation': 'Fast for 8-12 hours before the test. Only water is allowed.',
    },
    {
        'name': 'HbA1c (Glycated Haemoglobin)',
        'description': 'Shows average blood sugar levels over the past 2-3 months for long-term diabetes control.',
        'price': 400,
        'category': 'blood',
        'preparation': 'No fasting required.',
    },
    {
        'name': 'Thyroid Profile (T3, T4, TSH)',
        'description': 'Evaluates thyroid gland function and helps diagnose hypothyroidism or hyperthyroidism.',
        'price': 500,
        'category': 'blood',
        'preparation': 'Fasting recommended for 8 hours. Inform the lab about thyroid medication.',
    },
    {
        'name': 'Lipid Profile',
        'description': 'Measures cholesterol, HDL, LDL and triglycerides to assess cardiovascular risk.',
        'price': 450,
        'category': 'blood',
        'preparation': 'Fast for 9-12 hours before the test. Water is allowed.',
    },
    {
        'name': 'Liver Function Test (LFT)',
        'description': 'Checks enzymes and proteins produced by the liver to detect liver damage or disease.',
        'price': 500,
        'category': 'blood',
        'preparation': 'Fasting recommended for 8-10 hours.',
    },
    {
        'name': 'Kidney Function Test (KFT)',
        'description': 'Measures creatinine, urea and electrolytes to evaluate kidney health.',
        'price': 450,
        'category': 'blood',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Vitamin D (25-OH)',
        'description': 'Measures vitamin D levels to assess bone health and deficiency.',
        'price': 800,
        'category': 'blood',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Vitamin B12',
        'description': 'Measures vitamin B12 levels important for nerve function and red blood cell formation.',
        'price': 700,
        'category': 'blood',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Iron Studies Panel',
        'description': 'Measures serum iron, ferritin and TIBC to evaluate iron deficiency and anaemia.',
        'price': 900,
        'category': 'blood',
        'preparation': 'Fasting recommended for 8-10 hours.',
    },
    {
        'name': 'Urine Routine & Microscopy',
        'description': 'Examines physical, chemical and microscopic properties of urine to detect infections and kidney issues.',
        'price': 200,
        'category': 'urine',
        'preparation': 'Collect a mid-stream morning urine sample in a sterile container.',
    },
    {
        'name': 'Urine Culture & Sensitivity',
        'description': 'Identifies bacteria causing urinary tract infections and tests antibiotic sensitivity.',
        'price': 550,
        'category': 'urine',
        'preparation': 'Mid-stream urine sample in sterile container. Avoid antibiotics before collection.',
    },
    {
        'name': '24-Hour Urine Protein',
        'description': 'Measures total protein excreted in urine over 24 hours to assess kidney function.',
        'price': 650,
        'category': 'urine',
        'preparation': 'Collect all urine over 24 hours as instructed. Keep refrigerated.',
    },
    {
        'name': 'Chest X-Ray (PA View)',
        'description': 'Imaging of the chest to evaluate lungs, heart and rib cage for infections or abnormalities.',
        'price': 600,
        'category': 'imaging',
        'preparation': 'Remove metal jewellery. Wear comfortable clothing.',
    },
    {
        'name': 'X-Ray of Joint (Knee/Shoulder)',
        'description': 'Imaging of a specific joint to evaluate fractures, arthritis and joint damage.',
        'price': 550,
        'category': 'imaging',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Abdominal Ultrasound',
        'description': 'Ultrasound of abdomen to examine liver, gallbladder, pancreas, kidneys and spleen.',
        'price': 1200,
        'category': 'imaging',
        'preparation': 'Fast for 6-8 hours before the scan.',
    },
    {
        'name': 'ECG (Electrocardiogram)',
        'description': 'Records electrical activity of the heart to detect rhythm problems and heart conditions.',
        'price': 350,
        'category': 'cardiac',
        'preparation': 'No special preparation required. Avoid heavy meals before the test.',
    },
    {
        'name': '2D Echo (Echocardiography)',
        'description': 'Ultrasound of the heart to evaluate heart structure, valves and pumping function.',
        'price': 1800,
        'category': 'cardiac',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'TMT (Treadmill Test)',
        'description': 'Exercise stress test to evaluate heart function during physical activity.',
        'price': 1500,
        'category': 'cardiac',
        'preparation': 'Avoid caffeine and smoking for 3 hours before. Wear comfortable shoes.',
    },
    {
        'name': 'Total IgE (Allergy Screen)',
        'description': 'Measures total immunoglobulin E levels to detect allergic conditions.',
        'price': 850,
        'category': 'allergy',
        'preparation': 'No special preparation required. Inform about antihistamine medication.',
    },
    {
        'name': 'Allergy Panel (Common 20 Allergens)',
        'description': 'Screens for sensitivity to 20 common allergens including dust mites, pollens, foods and pet dander.',
        'price': 3500,
        'category': 'allergy',
        'preparation': 'Inform the lab about antihistamine and steroid medications.',
    },
    {
        'name': 'Full Body Checkup (Basic)',
        'description': 'Comprehensive screening including CBC, blood sugar, lipid profile, liver and kidney function tests.',
        'price': 1999,
        'category': 'general',
        'preparation': 'Fast for 10-12 hours before the test. Water is allowed.',
    },
    {
        'name': 'Full Body Checkup (Advanced)',
        'description': 'Extensive health screening with thyroid profile, vitamin levels, cancer markers and cardiac tests.',
        'price': 4499,
        'category': 'general',
        'preparation': 'Fast for 10-12 hours before the test. Water is allowed.',
    },
    {
        'name': 'Pregnancy Profile',
        'description': 'Essential tests for expectant mothers including CBC, blood group, blood sugar and infection screening.',
        'price': 1800,
        'category': 'general',
        'preparation': 'Fasting recommended for 8 hours.',
    },
    {
        'name': 'Dengue NS1 Antigen',
        'description': 'Detects dengue virus in the first 5 days of fever for early diagnosis.',
        'price': 950,
        'category': 'general',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Malaria Antigen Test',
        'description': 'Rapid detection of malaria parasites in the blood.',
        'price': 400,
        'category': 'general',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Widal Test (Typhoid)',
        'description': 'Screening test for typhoid fever antibodies in the blood.',
        'price': 350,
        'category': 'general',
        'preparation': 'No special preparation required.',
    },
    {
        'name': 'Uric Acid Test',
        'description': 'Measures uric acid levels to evaluate gout and kidney function.',
        'price': 300,
        'category': 'general',
        'preparation': 'Fast for 8 hours before the test.',
    },
]

BLOG_POSTS = [
    {
        'title': '10 Everyday Habits for a Healthier Heart',
        'excerpt': 'Simple, sustainable habits that can significantly reduce your risk of heart disease.',
        'content': '''
<h2>Why Heart Health Matters</h2>
<p>Heart disease remains one of the leading causes of death worldwide, but the good news is that most risk factors are within our control. Small, consistent habits can make a big difference over time.</p>

<h2>1. Walk 30 Minutes a Day</h2>
<p>A brisk daily walk strengthens your heart muscle, improves circulation and helps manage weight. You don't need a gym - a 30-minute walk after meals is enough to see measurable benefits.</p>

<h2>2. Eat More Whole Foods</h2>
<p>Focus on fruits, vegetables, whole grains and lean proteins. Reduce processed foods, excess salt and trans fats. A diet rich in fibre helps lower cholesterol naturally.</p>

<h2>3. Manage Stress with Deep Breathing</h2>
<p>Chronic stress raises cortisol and blood pressure. Practice 5-10 minutes of deep breathing or meditation daily to keep your stress levels in check.</p>

<h2>4. Sleep 7-8 Hours</h2>
<p>Poor sleep is linked to higher blood pressure and inflammation. Aim for 7-8 hours of quality sleep every night.</p>

<h2>5. Know Your Numbers</h2>
<p>Get your blood pressure, blood sugar and cholesterol checked regularly. Early detection of a problem is the first step to managing it.</p>

<h2>6. Quit Smoking and Limit Alcohol</h2>
<p>Smoking damages blood vessels and doubles heart attack risk. If you smoke, seek help to quit - your heart will thank you.</p>

<h2>7. Stay Hydrated</h2>
<p>Drinking enough water helps blood circulate more easily. Aim for 8 glasses a day, more in hot weather.</p>

<h2>8. Keep a Healthy Weight</h2>
<p>Excess weight strains the heart. Even losing 5-10% of your body weight can significantly lower blood pressure and cholesterol.</p>

<h2>9. Stay Socially Connected</h2>
<p>Loneliness is a surprising risk factor for heart disease. Stay connected with family and friends - it's good for your heart.</p>

<h2>10. Get Regular Health Checkups</h2>
<p>Annual checkups can catch problems early. Book a full body checkup or at least a cardiac risk assessment once a year.</p>

<h3>Remember</h3>
<p>Heart health is a marathon, not a sprint. Start with one or two habits and build from there. Your future self will thank you.</p>
''',
        'category': 'Wellness',
        'tags': 'heart, health, wellness, lifestyle',
    },
    {
        'title': 'Understanding Diabetes: Types, Symptoms and Management',
        'excerpt': 'A complete guide to diabetes - from understanding the types to everyday management.',
        'content': '''
<h2>What is Diabetes?</h2>
<p>Diabetes is a chronic condition where the body cannot properly process sugar (glucose), leading to high blood sugar levels. It affects how your body uses insulin, the hormone that regulates blood sugar.</p>

<h2>Types of Diabetes</h2>
<h3>Type 1 Diabetes</h3>
<p>An autoimmune condition where the body attacks insulin-producing cells in the pancreas. It usually appears in childhood or young adulthood and requires daily insulin injections.</p>

<h3>Type 2 Diabetes</h3>
<p>The most common type, often linked to lifestyle factors like obesity and inactivity. The body becomes resistant to insulin or doesn't produce enough. It can often be managed with diet, exercise and medication.</p>

<h3>Gestational Diabetes</h3>
<p>Occurs during pregnancy and usually resolves after childbirth, but increases the risk of developing Type 2 diabetes later.</p>

<h2>Common Symptoms</h2>
<ul>
<li>Frequent urination, especially at night</li>
<li>Excessive thirst and hunger</li>
<li>Unexplained weight loss</li>
<li>Fatigue and weakness</li>
<li>Blurred vision</li>
<li>Slow-healing wounds</li>
</ul>

<h2>Managing Diabetes</h2>
<h3>Monitor Blood Sugar Regularly</h3>
<p>Regular monitoring helps you understand how food, activity and medication affect your blood sugar. Aim for fasting levels between 70-130 mg/dL as recommended by your doctor.</p>

<h3>Eat a Balanced Diet</h3>
<p>Choose whole grains, vegetables and lean proteins. Limit sugary drinks and refined carbohydrates. Consider sugar-free sweeteners as alternatives.</p>

<h3>Stay Active</h3>
<p>Exercise helps your body use insulin more effectively. Aim for at least 150 minutes of moderate activity per week.</p>

<h3>Take Medication as Prescribed</h3>
<p>Whether it's metformin or insulin, take your medication exactly as prescribed. Never stop without consulting your doctor.</p>

<h2>Regular Checkups are Essential</h2>
<p>Diabetes affects your eyes, kidneys, nerves and heart over time. Regular HbA1c tests, eye exams and kidney function tests are vital for early detection of complications.</p>

<h3>Living Well with Diabetes</h3>
<p>Diabetes is manageable. With the right care, diet and support, you can live a full and active life.</p>
''',
        'category': 'Medicine',
        'tags': 'diabetes, blood sugar, health, management',
    },
    {
        'title': 'Common Cold vs Flu: How to Tell the Difference',
        'excerpt': 'Both are respiratory infections, but they are not the same. Here is how to identify and treat them.',
        'content': '''
<h2>Introduction</h2>
<p>When you wake up with a sore throat and a runny nose, it's natural to wonder: is this just a cold, or something more serious like the flu? While they share symptoms, they are caused by different viruses and require different care.</p>

<h2>Key Differences</h2>
<table>
<tr><th>Symptom</th><th>Cold</th><th>Flu</th></tr>
<tr><td>Onset</td><td>Gradual</td><td>Sudden</td></tr>
<tr><td>Fever</td><td>Rare</td><td>Common (38°C or higher)</td></tr>
<tr><td>Body aches</td><td>Mild</td><td>Severe</td></tr>
<tr><td>Fatigue</td><td>Mild</td><td>Severe, can last weeks</td></tr>
<tr><td>Sneezing</td><td>Common</td><td>Sometimes</td></tr>
<tr><td>Cough</td><td>Mild to moderate</td><td>Dry, persistent</td></tr>
</table>

<h2>Symptoms of a Cold</h2>
<p>Cold symptoms develop gradually and are usually mild. You may experience a runny or stuffy nose, sneezing, sore throat and a mild cough. Fever is uncommon in adults.</p>

<h2>Symptoms of the Flu</h2>
<p>The flu hits suddenly. High fever, severe body aches, chills, fatigue and a dry cough are hallmarks. You may feel too unwell to get out of bed.</p>

<h2>Home Care Tips</h2>
<ul>
<li>Rest well and stay hydrated</li>
<li>Use saline nasal sprays for congestion</li>
<li>Gargle with warm salt water for a sore throat</li>
<li>Take paracetamol or ibuprofen for fever and pain</li>
<li>Use cough lozenges for throat irritation</li>
</ul>

<h2>When to See a Doctor</h2>
<p>Seek medical attention if you experience difficulty breathing, chest pain, a fever lasting more than 3 days, or symptoms that worsen after improving.</p>

<h2>Prevention</h2>
<p>Wash hands frequently, avoid touching your face, maintain distance from sick individuals, and consider the annual flu vaccine, especially for older adults and those with chronic conditions.</p>
''',
        'category': 'Medicine',
        'tags': 'cold, flu, cough, health',
    },
    {
        'title': '5 Ways to Boost Your Immunity Naturally',
        'excerpt': 'Practical, science-backed tips to strengthen your body\'s natural defences.',
        'content': '''
<h2>Your Immune System: Your Body's Defence Force</h2>
<p>Your immune system works around the clock to protect you from infections. While no single food or pill can guarantee immunity, a healthy lifestyle can definitely support it.</p>

<h2>1. Eat a Rainbow of Fruits and Vegetables</h2>
<p>Vitamin C from citrus fruits, zinc from nuts and seeds, and antioxidants from berries all support immune function. Aim for at least 5 servings of fruits and vegetables daily.</p>

<h2>2. Prioritise Sleep</h2>
<p>During deep sleep, your body produces infection-fighting cells. Adults who sleep less than 7 hours are more prone to colds and infections. Make sleep a non-negotiable.</p>

<h2>3. Manage Stress</h2>
<p>Chronic stress suppresses immune function. Practices like yoga, meditation and deep breathing lower cortisol levels and support immunity.</p>

<h2>4. Stay Active</h2>
<p>Moderate exercise like brisk walking or cycling boosts immune cell circulation. Aim for 30 minutes of activity most days of the week.</p>

<h2>5. Stay Hydrated and Maintain Gut Health</h2>
<p>Probiotics like curd and yoghurt support gut bacteria, which play a key role in immunity. Drink enough water to keep your systems running smoothly.</p>

<h2>Supplements That Help</h2>
<p>Vitamin D, vitamin C, zinc and omega-3 supplements can help fill nutritional gaps, especially in winter or for those with deficiencies. Consult your doctor before starting any supplement.</p>

<h3>The Bottom Line</h3>
<p>Immunity is built daily through consistent habits, not quick fixes. Combine good nutrition, sleep, exercise and stress management for the best results.</p>
''',
        'category': 'Wellness',
        'tags': 'immunity, wellness, vitamins, health',
    },
    {
        'title': 'A Parent\'s Guide to Managing Fever in Children',
        'excerpt': 'Fever in kids can be alarming. Learn when to treat at home and when to see a doctor.',
        'content': '''
<h2>Understanding Fever in Children</h2>
<p>A fever is the body's natural response to infection - it means the immune system is fighting back. Most fevers in children are viral and resolve within 2-3 days.</p>

<h2>What Counts as a Fever?</h2>
<p>A temperature of 100.4°F (38°C) or higher is considered a fever. Temperatures up to 102°F are generally safe and do not need aggressive treatment if the child is comfortable.</p>

<h2>Home Care Tips</h2>
<ul>
<li>Keep the child hydrated with water, ORS or diluted fruit juices</li>
<li>Dress the child in light clothing - do not overdress or wrap in blankets</li>
<li>Encourage rest and quiet activities</li>
<li>Use paracetamol (calpol) or ibuprofen as per the weight-based dose from your paediatrician</li>
<li>Wipe with a lukewarm cloth if the child is uncomfortable</li>
</ul>

<h2>When to See a Doctor Immediately</h2>
<ul>
<li>Infant under 3 months with any fever</li>
<li>Fever above 104°F (40°C)</li>
<li>Fever lasting more than 3 days</li>
<li>Child is lethargic, confused or difficult to wake</li>
<li>Difficulty breathing or rapid breathing</li>
<li>Rash, stiff neck, or repeated vomiting</li>
<li>Signs of dehydration - dry mouth, no tears, no urine for 6+ hours</li>
</ul>

<h2>What NOT to Do</h2>
<p>Never give aspirin to children - it can cause Reye's syndrome, a rare but serious condition. Avoid cold baths and alcohol rubs, which can cause shivering and discomfort.</p>

<h2>When the Fever Breaks</h2>
<p>Once the fever subsides, ensure the child continues to rest and hydrate. Follow up with your paediatrician if symptoms persist or new symptoms appear.</p>
''',
        'category': 'Parenting',
        'tags': 'children, fever, parenting, health',
    },
    {
        'title': 'Vitamins and Minerals: A Complete Daily Guide',
        'excerpt': 'Everything you need to know about essential vitamins, their sources and daily requirements.',
        'content': '''
<h2>Why Vitamins Matter</h2>
<p>Vitamins and minerals are essential for every function in your body - from energy production to immune defence. Most can be obtained from a balanced diet, but deficiencies are surprisingly common.</p>

<h2>Vitamin A</h2>
<p><strong>Role:</strong> Vision, immune function, skin health<br/>
<strong>Sources:</strong> Carrots, sweet potato, spinach, eggs, milk<br/>
<strong>Deficiency signs:</strong> Night blindness, dry skin</p>

<h2>Vitamin B-Complex</h2>
<p><strong>Role:</strong> Energy metabolism, nerve function, red blood cell formation<br/>
<strong>Sources:</strong> Whole grains, eggs, meat, legumes, leafy greens<br/>
<strong>Deficiency signs:</strong> Fatigue, anaemia, tingling in hands and feet</p>

<h2>Vitamin C</h2>
<p><strong>Role:</strong> Immunity, collagen formation, antioxidant<br/>
<strong>Sources:</strong> Citrus fruits, amla, guava, bell peppers<br/>
<strong>Deficiency signs:</strong> Frequent infections, slow wound healing, bleeding gums</p>

<h2>Vitamin D</h2>
<p><strong>Role:</strong> Calcium absorption, bone health, immunity<br/>
<strong>Sources:</strong> Sunlight, fortified milk, fatty fish, supplements<br/>
<strong>Deficiency signs:</strong> Bone pain, muscle weakness, frequent illness</p>

<h2>Calcium</h2>
<p><strong>Role:</strong> Bone and teeth health, muscle function, nerve signalling<br/>
<strong>Sources:</strong> Milk, curd, paneer, ragi, leafy greens<br/>
<strong>Deficiency signs:</strong> Weak bones, muscle cramps</p>

<h2>Iron</h2>
<p><strong>Role:</strong> Oxygen transport in blood, energy<br/>
<strong>Sources:</strong> Red meat, spinach, beans, fortified cereals<br/>
<strong>Deficiency signs:</strong> Fatigue, pale skin, breathlessness, anaemia</p>

<h2>Zinc</h2>
<p><strong>Role:</strong> Immunity, wound healing, growth<br/>
<strong>Sources:</strong> Nuts, seeds, meat, legumes<br/>
<strong>Deficiency signs:</strong> Hair loss, frequent infections, poor appetite</p>

<h2>Who Needs Supplements?</h2>
<p>Vegetarians often need vitamin B12 supplements, office workers commonly lack vitamin D, and women of childbearing age may need iron and folic acid. Always get tested before starting supplements.</p>

<h2>Get Tested</h2>
<p>Regular blood tests like vitamin D, vitamin B12 and iron studies can reveal silent deficiencies. Early correction prevents long-term health problems.</p>
''',
        'category': 'Nutrition',
        'tags': 'vitamins, minerals, nutrition, supplements',
    },
    {
        'title': 'Reading Your Blood Test Results: A Beginner\'s Guide',
        'excerpt': 'Confused by your lab report? Here is how to understand the key numbers.',
        'content': '''
<h2>Your Lab Report Explained</h2>
<p>Lab results can look intimidating, but understanding the basics empowers you to have better conversations with your doctor.</p>

<h2>Complete Blood Count (CBC)</h2>
<h3>Haemoglobin (Hb)</h3>
<p><strong>Normal range:</strong> 13-17 g/dL (men), 12-15 g/dL (women)<br/>
Low levels indicate anaemia; high levels may suggest dehydration or lung conditions.</p>

<h3>White Blood Cells (WBC)</h3>
<p><strong>Normal range:</strong> 4,000-11,000 /µL<br/>
Elevated WBC often indicates infection or inflammation. Low WBC may suggest viral infections or immune disorders.</p>

<h3>Platelets</h3>
<p><strong>Normal range:</strong> 150,000-450,000 /µL<br/>
Low platelets increase bleeding risk; high counts may suggest inflammation or marrow issues.</p>

<h2>Blood Sugar</h2>
<h3>Fasting Blood Sugar</h3>
<p><strong>Normal:</strong> Below 100 mg/dL<br/>
<strong>Prediabetic:</strong> 100-125 mg/dL<br/>
<strong>Diabetic:</strong> 126 mg/dL or above</p>

<h2>Lipid Profile</h2>
<h3>Total Cholesterol</h3>
<p><strong>Desirable:</strong> Below 200 mg/dL<br/>
<h3>LDL (Bad Cholesterol)</h3>
<p><strong>Optimal:</strong> Below 100 mg/dL</p>
<h3>HDL (Good Cholesterol)</h3>
<p><strong>Optimal:</strong> Above 60 mg/dL</p>

<h2>Thyroid (TSH)</h2>
<p><strong>Normal range:</strong> 0.4-4.0 mIU/L<br/>
Elevated TSH suggests hypothyroidism; suppressed TSH points to hyperthyroidism.</p>

<h2>Liver Function</h2>
<p>SGOT, SGPT and ALP are key liver enzymes. Mild elevations are common after alcohol, fatty meals or medications; persistent elevations need evaluation.</p>

<h2>Kidney Function</h2>
<p>Creatinine (normal: 0.6-1.2 mg/dL) and blood urea are markers of kidney health. Persistent elevation warrants a nephrology consult.</p>

<h2>Important Reminders</h2>
<ul>
<li>Reference ranges vary slightly between labs</li>
<li>Never self-diagnose - your doctor interprets results in context</li>
<li>Take medication as prescribed even if you feel fine</li>
</ul>
''',
        'category': 'Medicine',
        'tags': 'lab test, blood test, health, diagnosis',
    },
    {
        'title': 'Home Remedies That Actually Work for Acidity and Heartburn',
        'excerpt': 'Fast relief for that burning sensation, plus habits to prevent it from coming back.',
        'content': '''
<h2>Understanding Acidity</h2>
<p>Acidity occurs when stomach acid flows back into the food pipe, causing a burning sensation in the chest and throat. Spicy food, stress, smoking and irregular eating habits are common triggers.</p>

<h2>Quick Relief Home Remedies</h2>
<h3>1. Cold Milk</h3>
<p>A glass of cold milk neutralises stomach acid instantly. Its calcium content provides soothing relief.</p>

<h3>2. Cumin Water (Jeera Water)</h3>
<p>Boil a teaspoon of cumin in water and drink it warm. Cumin stimulates digestive enzymes and soothes the stomach lining.</p>

<h3>3. Ginger Tea</h3>
<p>Ginger has natural anti-inflammatory properties. A small piece in hot water helps reduce acid reflux.</p>

<h3>4. Fennel Seeds (Saunf)</h3>
<p>Chewing fennel seeds after meals aids digestion and freshens breath. They're a natural antacid.</p>

<h3>5. Buttermilk</h3>
<p>Lactic acid in buttermilk soothes the stomach. Add a pinch of roasted cumin for better effect.</p>

<h2>Over-the-Counter Options</h2>
<p>Antacids like Digene or Gelusil provide quick relief for occasional acidity. For frequent symptoms, H2 blockers like ranitidine or proton pump inhibitors may be recommended by your doctor.</p>

<h2>Prevention Habits</h2>
<ul>
<li>Eat smaller, more frequent meals</li>
<li>Avoid lying down immediately after eating - wait 2-3 hours</li>
<li>Limit spicy, oily and acidic foods</li>
<li>Elevate your head while sleeping</li>
<li>Maintain a healthy weight</li>
<li>Quit smoking and limit alcohol</li>
</ul>

<h2>When to See a Doctor</h2>
<p>Seek medical help if you have heartburn more than twice a week, difficulty swallowing, persistent nausea, or symptoms that don't respond to antacids. Chronic acidity can damage the food pipe over time.</p>
''',
        'category': 'Wellness',
        'tags': 'acidity, heartburn, digestion, home remedies',
    },
    {
        'title': 'Sleep Hygiene: 10 Rules for Better Sleep Tonight',
        'excerpt': 'Struggling to sleep? These science-backed habits can transform your nights.',
        'content': '''
<h2>The Importance of Sleep</h2>
<p>Sleep is when your body repairs itself, consolidates memory and resets hormones. Poor sleep is linked to obesity, diabetes, heart disease and poor mental health.</p>

<h2>Rule 1: Fix Your Wake-Up Time</h2>
<p>A consistent wake-up time anchors your body clock. Even on weekends, try to wake within an hour of your usual time.</p>

<h2>Rule 2: Get Morning Sunlight</h2>
<p>Exposure to morning light within 30 minutes of waking sets your circadian rhythm for the day.</p>

<h2>Rule 3: Create a Wind-Down Routine</h2>
<p>Dim lights, read a book, or take a warm shower 30-60 minutes before bed. This signals your brain that it's time to sleep.</p>

<h2>Rule 4: No Screens an Hour Before Bed</h2>
<p>Blue light from phones and laptops suppresses melatonin, the sleep hormone. Keep devices out of the bedroom.</p>

<h2>Rule 5: Keep the Room Cool and Dark</h2>
<p>Your body sleeps best at around 18-20°C. Use blackout curtains and consider a sleep mask.</p>

<h2>Rule 6: Limit Caffeine After 2 PM</h2>
<p>Caffeine has a half-life of 5-6 hours. That afternoon coffee may still be affecting you at midnight.</p>

<h2>Rule 7: Avoid Heavy Meals Late</h2>
<p>Eating large meals close to bedtime can cause discomfort and disrupt sleep. Finish dinner 3 hours before bed.</p>

<h2>Rule 8: Limit Alcohol</h2>
<p>Alcohol may make you drowsy, but it fragments sleep and reduces sleep quality.</p>

<h2>Rule 9: Exercise Daily</h2>
<p>Regular exercise promotes deeper sleep. Just avoid vigorous workouts within 2 hours of bedtime.</p>

<h2>Rule 10: If You Can't Sleep, Get Up</h2>
<p>If you're lying awake for more than 20 minutes, get up and do something relaxing in dim light until you feel sleepy.</p>

<h3>When to Seek Help</h3>
<p>If poor sleep persists for over a month despite good habits, consult a doctor. You may have insomnia or sleep apnoea that needs treatment.</p>
''',
        'category': 'Wellness',
        'tags': 'sleep, insomnia, wellness, health',
    },
    {
        'title': 'First Aid Essentials Every Home Must Have',
        'excerpt': 'Be prepared for emergencies with this complete home first aid checklist.',
        'content': '''
<h2>Why Every Home Needs a First Aid Kit</h2>
<p>Accidents happen - a kitchen cut, a burn, a fall, or a sprain. Having the right supplies at home can make the difference between a minor inconvenience and a medical emergency.</p>

<h2>The Essentials Checklist</h2>
<h3>Bandages and Dressings</h3>
<ul>
<li>Adhesive bandages in multiple sizes (Band-Aid)</li>
<li>Sterile gauze pads (various sizes)</li>
<li>Rolled gauze bandages</li>
<li>Elastic/crepe bandages for sprains</li>
<li>Surgical adhesive tape</li>
<li>Triangular bandage for slings</li>
</ul>

<h3>Tools</h3>
<ul>
<li>Tweezers for splinters</li>
<li>Scissors with rounded tips</li>
<li>Instant ice packs</li>
<li>Digital thermometer</li>
<li>Gloves (nitrile preferred)</li>
</ul>

<h3>Medications and Antiseptics</h3>
<ul>
<li>Antiseptic solution or wipes (Dettol/Savlon)</li>
<li>Antibiotic ointment (Soframycin/Neosporin)</li>
<li>Burn relief cream (Burnol)</li>
<li>Paracetamol for fever and pain</li>
<li>Oral rehydration salts</li>
<li>Antihistamines for allergies</li>
<li>Hydrocortisone cream for rashes</li>
</ul>

<h3>Special Items</h3>
<ul>
<li>CPR face shield</li>
<li>Emergency thermal blanket</li>
<li>Eye wash solution</li>
<li>Alcohol swabs</li>
<li>Cotton wool and buds</li>
</ul>

<h2>Storage and Maintenance</h2>
<ul>
<li>Store in a cool, dry place away from children</li>
<li>Check expiry dates every 6 months</li>
<li>Keep a list of emergency contacts inside the kit</li>
<li>Replace used items immediately</li>
</ul>

<h2>Basic First Aid: What to Do</h2>
<h3>For Cuts</h3>
<p>Clean with running water, apply antiseptic, cover with a sterile dressing.</p>
<h3>For Burns</h3>
<p>Cool the burn under running water for 10-15 minutes, cover with a clean cloth, never apply ice directly.</p>
<h3>For Sprains</h3>
<p>Rest, ice, compression, elevation - the RICE method.</p>

<h2>When to Call Emergency Services</h2>
<p>Severe bleeding, difficulty breathing, chest pain, unconsciousness, or suspected fractures require immediate professional help.</p>
''',
        'category': 'Safety',
        'tags': 'first aid, safety, emergency, home',
    },
    {
        'title': 'Blood Pressure Management: A Complete Guide',
        'excerpt': 'Understand hypertension, monitor your numbers and take control of your heart health.',
        'content': '''
<h2>Understanding Blood Pressure</h2>
<p>Blood pressure is the force of blood against your artery walls. It's recorded as two numbers: systolic (pressure during heartbeats) and diastolic (pressure between beats).</p>

<h2>What the Numbers Mean</h2>
<table>
<tr><th>Category</th><th>Systolic</th><th>Diastolic</th></tr>
<tr><td>Normal</td><td>Below 120</td><td>Below 80</td></tr>
<tr><td>Elevated</td><td>120-129</td><td>Below 80</td></tr>
<tr><td>Hypertension Stage 1</td><td>130-139</td><td>80-89</td></tr>
<tr><td>Hypertension Stage 2</td><td>140+</td><td>90+</td></tr>
</table>

<h2>The Silent Danger</h2>
<p>Hypertension rarely causes symptoms, which is why it's called the "silent killer". Left uncontrolled, it damages your heart, brain, kidneys and eyes.</p>

<h2>Lifestyle Changes That Work</h2>
<h3>Reduce Salt Intake</h3>
<p>Limit sodium to under 5g (1 teaspoon) per day. Avoid processed foods, pickles and packaged snacks.</p>

<h3>Exercise Regularly</h3>
<p>150 minutes of moderate exercise weekly can lower systolic pressure by 5-8 mmHg.</p>

<h3>Maintain a Healthy Weight</h3>
<p>Each kilogram lost can reduce blood pressure by roughly 1 mmHg.</p>

<h3>Limit Alcohol and Quit Smoking</h3>
<p>Both raise blood pressure and damage blood vessels.</p>

<h2>Monitoring at Home</h2>
<p>Home monitors are reliable when used correctly. Sit quietly for 5 minutes, place the cuff on a bare arm at heart level, and take readings at the same time daily. Record your numbers for your doctor.</p>

<h2>Medication Adherence</h2>
<p>If prescribed medication like amlodipine, telmisartan or losartan, take it daily at the same time. Never stop without medical advice - high blood pressure is often a lifelong condition that requires ongoing treatment.</p>

<h2>When to Seek Immediate Help</h2>
<p>Blood pressure above 180/120 with chest pain, shortness of breath, or neurological symptoms is a medical emergency.</p>
''',
        'category': 'Medicine',
        'tags': 'blood pressure, hypertension, heart, health',
    },
]


class Command(BaseCommand):
    help = 'Seed lab tests and health blog posts'

    def add_arguments(self, parser):
        parser.add_argument('--lab-only', action='store_true')
        parser.add_argument('--blog-only', action='store_true')

    def handle(self, *args, **options):
        lab_only = options['lab_only']
        blog_only = options['blog_only']

        if not blog_only:
            lab_created = 0
            lab_existing = 0
            for t in LAB_TESTS:
                _, created = LabTest.objects.get_or_create(
                    name=t['name'],
                    defaults={
                        'description': t['description'],
                        'price': t['price'],
                        'category': t['category'],
                        'preparation_instructions': t['preparation'],
                        'is_active': True,
                    },
                )
                if created:
                    lab_created += 1
                else:
                    lab_existing += 1
            self.stdout.write(self.style.SUCCESS(
                f'Lab tests: {lab_created} created, {lab_existing} existing'
            ))

        if not lab_only:
            blog_created = 0
            blog_existing = 0
            for post in BLOG_POSTS:
                slug = slugify(post['title'])[:50]
                _, created = BlogPost.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'title': post['title'],
                        'excerpt': post['excerpt'],
                        'content': post['content'],
                        'category': post['category'],
                        'tags': post['tags'],
                        'is_published': True,
                    },
                )
                if created:
                    blog_created += 1
                else:
                    blog_existing += 1
            self.stdout.write(self.style.SUCCESS(
                f'Blog posts: {blog_created} created, {blog_existing} existing'
            ))
