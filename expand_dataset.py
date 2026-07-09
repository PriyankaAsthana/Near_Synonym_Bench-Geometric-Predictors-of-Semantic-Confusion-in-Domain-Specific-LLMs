import json

with open("data/concept_pairs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ADDITIONAL_MEDICAL = [
    {
        "id": "med_011",
        "term_a": "type 1 diabetes",
        "term_b": "type 2 diabetes",
        "distinction": "Type 1 diabetes is an autoimmune condition where the pancreas produces no insulin. Type 2 diabetes is a metabolic condition where the body becomes resistant to insulin. Type 1 requires insulin injections for survival. Type 2 is often managed with lifestyle changes and oral medication.",
        "stakes": "high",
        "correct_context": "A child diagnosed with diabetes whose pancreas produces zero insulin has type 1. An overweight adult whose cells stop responding to insulin has type 2.",
        "confusion_probe": "A 10-year-old child is diagnosed with diabetes and told their pancreas produces no insulin at all and they will require insulin injections for life. What type of diabetes is this?",
        "correct_answer": "type 1 diabetes",
        "confused_answer": "type 2 diabetes"
    },
    {
        "id": "med_012",
        "term_a": "tachycardia",
        "term_b": "bradycardia",
        "distinction": "Tachycardia is an abnormally fast heart rate above 100 beats per minute. Bradycardia is an abnormally slow heart rate below 60 beats per minute. Both are arrhythmias but require opposite interventions.",
        "stakes": "high",
        "correct_context": "A resting heart rate of 140 bpm is tachycardia. A resting heart rate of 35 bpm is bradycardia.",
        "confusion_probe": "A patient in the emergency department has a heart rate of 160 beats per minute at rest. What arrhythmia is this?",
        "correct_answer": "tachycardia",
        "confused_answer": "bradycardia"
    },
    {
        "id": "med_013",
        "term_a": "benign tumor",
        "term_b": "malignant tumor",
        "distinction": "A benign tumor is non-cancerous, does not invade nearby tissue, and does not spread to other parts of the body. A malignant tumor is cancerous, invades surrounding tissue, and can metastasize.",
        "stakes": "high",
        "correct_context": "A slow-growing encapsulated lump that stays in one place is benign. A tumor that invades muscle and spreads to lymph nodes is malignant.",
        "confusion_probe": "A tumor found in a patient's breast is encapsulated, has not invaded surrounding tissue, and shows no signs of spreading. What type of tumor is this?",
        "correct_answer": "benign tumor",
        "confused_answer": "malignant tumor"
    },
    {
        "id": "med_014",
        "term_a": "acute pain",
        "term_b": "chronic pain",
        "distinction": "Acute pain is short-term pain that arises suddenly from a specific cause and resolves as healing occurs. Chronic pain persists for more than 3 months, often beyond the original cause.",
        "stakes": "medium",
        "correct_context": "Pain immediately after surgery that resolves over weeks is acute. Pain persisting for years after an injury with no clear ongoing cause is chronic.",
        "confusion_probe": "A patient who broke their arm 2 weeks ago is experiencing pain at the fracture site that is gradually improving. What type of pain is this?",
        "correct_answer": "acute pain",
        "confused_answer": "chronic pain"
    },
    {
        "id": "med_015",
        "term_a": "arteries",
        "term_b": "veins",
        "distinction": "Arteries carry oxygenated blood away from the heart to the body. Veins carry deoxygenated blood back to the heart. The pulmonary artery is an exception — it carries deoxygenated blood from heart to lungs.",
        "stakes": "high",
        "correct_context": "The aorta carries oxygen-rich blood from the heart to the body — it is an artery. The vena cava returns oxygen-depleted blood to the heart — it is a vein.",
        "confusion_probe": "The blood vessels that carry oxygenated blood away from the heart to supply organs and tissues are called what?",
        "correct_answer": "arteries",
        "confused_answer": "veins"
    },
    {
        "id": "med_016",
        "term_a": "antibiotic",
        "term_b": "antiviral",
        "distinction": "Antibiotics treat bacterial infections by killing or inhibiting bacteria. Antivirals treat viral infections. Antibiotics have no effect on viruses. Using antibiotics for viral infections causes antibiotic resistance.",
        "stakes": "high",
        "correct_context": "Amoxicillin prescribed for bacterial pneumonia is an antibiotic. Oseltamivir prescribed for influenza is an antiviral.",
        "confusion_probe": "A patient has influenza caused by a virus. The correct medication class to prescribe is what?",
        "correct_answer": "antiviral",
        "confused_answer": "antibiotic"
    },
    {
        "id": "med_017",
        "term_a": "immunity",
        "term_b": "immunisation",
        "distinction": "Immunity is the state of being protected against a disease. Immunisation is the process by which immunity is acquired through vaccination.",
        "stakes": "medium",
        "correct_context": "A person who cannot get measles because their immune system recognises the virus has immunity. The act of giving a measles vaccine to create that protection is immunisation.",
        "confusion_probe": "The process of administering a vaccine to a child to protect them against polio is called what?",
        "correct_answer": "immunisation",
        "confused_answer": "immunity"
    },
    {
        "id": "med_018",
        "term_a": "sign",
        "term_b": "symptom",
        "distinction": "A symptom is what the patient reports experiencing — subjective. A sign is what a clinician observes or measures — objective.",
        "stakes": "medium",
        "correct_context": "A patient saying they feel hot is a symptom. A doctor measuring a temperature of 39 degrees Celsius is a sign.",
        "confusion_probe": "A doctor measures a patient's blood pressure and finds it is 180/110 mmHg. This observed measurement is called what?",
        "correct_answer": "sign",
        "confused_answer": "symptom"
    },
    {
        "id": "med_019",
        "term_a": "prognosis",
        "term_b": "diagnosis",
        "distinction": "Diagnosis is the identification of a disease or condition. Prognosis is the predicted outcome or course of that condition.",
        "stakes": "medium",
        "correct_context": "Identifying that a patient has stage 3 lung cancer is the diagnosis. Estimating that the patient has an 18-month survival probability is the prognosis.",
        "confusion_probe": "After running tests, a doctor tells a patient they have type 2 diabetes. This identification of the condition is called what?",
        "correct_answer": "diagnosis",
        "confused_answer": "prognosis"
    },
    {
        "id": "med_020",
        "term_a": "contraindication",
        "term_b": "side effect",
        "distinction": "A contraindication is a condition that makes a particular treatment inadvisable or unsafe. A side effect is an unintended effect that occurs alongside the intended therapeutic effect.",
        "stakes": "high",
        "correct_context": "Aspirin being unsafe for patients with bleeding disorders is a contraindication. Aspirin causing stomach irritation in patients taking it for heart protection is a side effect.",
        "confusion_probe": "A patient taking ibuprofen for pain develops stomach irritation as an unintended result. This is called what?",
        "correct_answer": "side effect",
        "confused_answer": "contraindication"
    },
    {
        "id": "med_021",
        "term_a": "incidence",
        "term_b": "prevalence",
        "distinction": "Incidence is the number of new cases of a disease in a population over a specific time period. Prevalence is the total number of existing cases at a given point in time.",
        "stakes": "medium",
        "correct_context": "1000 new diabetes diagnoses in India in 2025 is incidence. 77 million people in India currently living with diabetes is prevalence.",
        "confusion_probe": "A study reports that 500 new cases of tuberculosis were diagnosed in a city during 2025. This figure represents what epidemiological measure?",
        "correct_answer": "incidence",
        "confused_answer": "prevalence"
    },
    {
        "id": "med_022",
        "term_a": "hematoma",
        "term_b": "edema",
        "distinction": "A hematoma is a localised collection of blood outside blood vessels, usually due to injury. Edema is swelling caused by excess fluid accumulation in tissue.",
        "stakes": "medium",
        "correct_context": "A bruise with pooled blood under the skin after a head injury is a hematoma. Swollen ankles in a patient with heart failure due to fluid buildup is edema.",
        "confusion_probe": "After a head injury, a patient develops a localised collection of blood beneath the skull pressing on the brain. What is this called?",
        "correct_answer": "hematoma",
        "confused_answer": "edema"
    },
    {
        "id": "med_023",
        "term_a": "dialysis",
        "term_b": "transplant",
        "distinction": "Dialysis is a procedure that artificially performs kidney filtration functions when kidneys fail. Transplant is the surgical replacement of a failed organ with a healthy donor organ.",
        "stakes": "high",
        "correct_context": "A patient with kidney failure attached to a machine three times weekly for blood filtration is on dialysis. A patient receiving a new kidney from a donor undergoes transplant.",
        "confusion_probe": "A patient with end-stage kidney failure has their blood filtered by a machine three times a week to remove waste. What procedure is this?",
        "correct_answer": "dialysis",
        "confused_answer": "transplant"
    },
    {
        "id": "med_024",
        "term_a": "prophylaxis",
        "term_b": "treatment",
        "distinction": "Prophylaxis is preventive action taken to prevent disease before it occurs. Treatment is intervention applied after a disease or condition has developed.",
        "stakes": "high",
        "correct_context": "Taking malaria medication before travelling to an endemic region is prophylaxis. Taking malaria medication after being diagnosed with malaria is treatment.",
        "confusion_probe": "A traveller takes antimalarial medication before visiting a malaria-endemic country to prevent infection. This preventive measure is called what?",
        "correct_answer": "prophylaxis",
        "confused_answer": "treatment"
    },
    {
        "id": "med_025",
        "term_a": "acute kidney injury",
        "term_b": "chronic kidney disease",
        "distinction": "Acute kidney injury is a sudden rapid loss of kidney function occurring over hours to days, often reversible. Chronic kidney disease is a gradual progressive loss of kidney function over months to years, generally irreversible.",
        "stakes": "high",
        "correct_context": "A patient whose kidneys stop working after a severe infection recovers kidney function after treatment — acute kidney injury. A diabetic patient whose kidney function has been gradually declining for 5 years — chronic kidney disease.",
        "confusion_probe": "A patient develops sudden kidney failure within 48 hours of a severe infection. After treatment the kidneys may recover. What is this condition called?",
        "correct_answer": "acute kidney injury",
        "confused_answer": "chronic kidney disease"
    }
]

ADDITIONAL_CULTURAL = [
    {
        "id": "cul_011",
        "term_a": "Vedas",
        "term_b": "Upanishads",
        "distinction": "The Vedas are the oldest sacred Hindu texts containing hymns, rituals, and cosmological knowledge. The Upanishads are later philosophical texts that form the concluding part of the Vedas, exploring the nature of reality, the self, and Brahman.",
        "stakes": "medium",
        "correct_context": "The Rigveda containing hymns to deities is a Veda. The Brihadaranyaka Upanishad exploring the nature of Brahman and Atman is an Upanishad.",
        "confusion_probe": "The ancient Hindu philosophical texts that explore the nature of the self and ultimate reality and form the concluding portion of the Vedic corpus are called what?",
        "correct_answer": "Upanishads",
        "confused_answer": "Vedas"
    },
    {
        "id": "cul_012",
        "term_a": "pilgrimage",
        "term_b": "tourism",
        "distinction": "Pilgrimage is travel to a sacred place for religious or spiritual purposes. Tourism is travel for leisure, recreation, or cultural exploration without religious motivation.",
        "stakes": "low",
        "correct_context": "Travelling to Varanasi to bathe in the Ganges for spiritual purification is pilgrimage. Travelling to Varanasi to photograph the ghats and experience the culture is tourism.",
        "confusion_probe": "A devout Hindu travels to Varanasi specifically to perform ritual bathing in the Ganges and seek spiritual merit. What type of journey is this?",
        "correct_answer": "pilgrimage",
        "confused_answer": "tourism"
    },
    {
        "id": "cul_013",
        "term_a": "tabla",
        "term_b": "mridangam",
        "distinction": "Tabla is a pair of hand drums used in Hindustani classical music of North India. Mridangam is a double-headed drum used in Carnatic classical music of South India.",
        "stakes": "medium",
        "correct_context": "The percussion instrument accompanying a sitar recital in Varanasi is tabla. The percussion instrument accompanying a veena recital in Chennai is mridangam.",
        "confusion_probe": "The pair of hand drums that accompanies Hindustani classical music performances in North India is called what?",
        "correct_answer": "tabla",
        "confused_answer": "mridangam"
    },
    {
        "id": "cul_014",
        "term_a": "Katan silk",
        "term_b": "Georgette",
        "distinction": "Katan silk is a pure silk fabric woven from raw silk threads used in traditional Banarasi sarees. Georgette is a lightweight crinkled fabric that can be silk or synthetic used in a different variety of Banarasi saree.",
        "stakes": "low",
        "correct_context": "The heaviest most traditional Banarasi saree variety woven from pure raw silk is Katan. The lighter crinkled variety of Banarasi saree is Georgette.",
        "confusion_probe": "The traditional Banarasi saree woven from pure raw silk threads producing a heavy lustrous fabric is called what variety?",
        "correct_answer": "Katan silk",
        "confused_answer": "Georgette"
    },
    {
        "id": "cul_015",
        "term_a": "Hindustani music",
        "term_b": "Carnatic music",
        "distinction": "Hindustani music is the classical music tradition of North India influenced by Persian and Mughal traditions. Carnatic music is the classical music tradition of South India with ancient Vedic roots.",
        "stakes": "medium",
        "correct_context": "The classical music tradition of Varanasi, Lucknow, and Delhi is Hindustani. The classical music tradition of Chennai, Thiruvananthapuram, and Mysore is Carnatic.",
        "confusion_probe": "The classical music tradition practiced in Varanasi that uses ragas, talas, and was influenced by Mughal court culture is called what?",
        "correct_answer": "Hindustani music",
        "confused_answer": "Carnatic music"
    },
    {
        "id": "cul_016",
        "term_a": "mantra",
        "term_b": "shloka",
        "distinction": "A mantra is a sacred sound, syllable, or phrase repeated during meditation or ritual for its spiritual power. A shloka is a verse from Hindu scriptures composed in a specific poetic meter.",
        "stakes": "low",
        "correct_context": "Om Namah Shivaya repeated during meditation is a mantra. A verse from the Bhagavad Gita composed in anushtubh meter is a shloka.",
        "confusion_probe": "The sacred syllables Om Namah Shivaya repeatedly chanted during Shiva worship for spiritual power are called what?",
        "correct_answer": "mantra",
        "confused_answer": "shloka"
    },
    {
        "id": "cul_017",
        "term_a": "avatar",
        "term_b": "deity",
        "distinction": "A deity is a divine being worshipped as a god. An avatar is a specific earthly incarnation or manifestation of a deity — particularly of Vishnu.",
        "stakes": "medium",
        "correct_context": "Vishnu is a deity. Rama and Krishna are avatars of Vishnu — earthly incarnations.",
        "confusion_probe": "Krishna, the divine figure who speaks the Bhagavad Gita, is considered an earthly incarnation of Vishnu. What is the correct term for this incarnation?",
        "correct_answer": "avatar",
        "confused_answer": "deity"
    },
    {
        "id": "cul_018",
        "term_a": "ashram",
        "term_b": "monastery",
        "distinction": "An ashram is a Hindu spiritual hermitage or community for spiritual practice under a guru. A monastery is a Buddhist or Christian institution where monks live under religious vows.",
        "stakes": "low",
        "correct_context": "A Hindu community where disciples live with a guru for spiritual learning is an ashram. A Buddhist institution where monks follow the Vinaya rules is a monastery.",
        "confusion_probe": "A community in Varanasi where Hindu disciples live with a spiritual teacher to practice yoga and meditation is called what?",
        "correct_answer": "ashram",
        "confused_answer": "monastery"
    },
    {
        "id": "cul_019",
        "term_a": "prasad",
        "term_b": "bhog",
        "distinction": "Bhog is food offered to a deity during worship. Prasad is the same food after it has been offered and blessed — distributed to devotees as a divine gift.",
        "stakes": "low",
        "correct_context": "The sweets placed before the deity during puja are bhog. The same sweets distributed to devotees after the deity has accepted the offering are prasad.",
        "confusion_probe": "The food that has been offered to a Hindu deity during worship and is then distributed to devotees as a blessed gift is called what?",
        "correct_answer": "prasad",
        "confused_answer": "bhog"
    },
    {
        "id": "cul_020",
        "term_a": "Ramcharitmanas",
        "term_b": "Ramayana",
        "distinction": "The Ramayana is the ancient Sanskrit epic by Valmiki. The Ramcharitmanas is a 16th century retelling of the Ramayana by Tulsidas written in Awadhi Hindi — venerated in North India especially in Varanasi.",
        "stakes": "medium",
        "correct_context": "The original Sanskrit epic of Rama composed by Valmiki is the Ramayana. The Awadhi version by Tulsidas kept at the Tulsi Manas Mandir in Varanasi is the Ramcharitmanas.",
        "confusion_probe": "The 16th century Awadhi language retelling of the story of Rama composed by the poet Tulsidas is called what?",
        "correct_answer": "Ramcharitmanas",
        "confused_answer": "Ramayana"
    },
    {
        "id": "cul_021",
        "term_a": "cremation ground",
        "term_b": "burial ground",
        "distinction": "A cremation ground is where Hindu and Buddhist dead are burned. A burial ground is where bodies are interred in the earth, common in Islamic and Christian traditions.",
        "stakes": "medium",
        "correct_context": "Manikarnika Ghat in Varanasi where Hindu bodies are burned is a cremation ground. A Muslim qabrastaan where bodies are buried is a burial ground.",
        "confusion_probe": "Manikarnika Ghat in Varanasi where Hindu bodies are ritually burned is called what type of sacred site?",
        "correct_answer": "cremation ground",
        "confused_answer": "burial ground"
    },
    {
        "id": "cul_022",
        "term_a": "sitar",
        "term_b": "sarod",
        "distinction": "Sitar is a long-necked plucked string instrument with movable frets, associated with Ravi Shankar and the Benares and Jaipur gharanas. Sarod is a fretless plucked string instrument with a deeper bass sound associated with the Gwalior gharana.",
        "stakes": "medium",
        "correct_context": "The instrument with movable frets played by Ravi Shankar in Hindustani music is sitar. The fretless instrument with a metal fingerboard played by Amjad Ali Khan is sarod.",
        "confusion_probe": "The long-necked fretted plucked string instrument most associated with Hindustani classical music and played by Ravi Shankar is called what?",
        "correct_answer": "sitar",
        "confused_answer": "sarod"
    },
    {
        "id": "cul_023",
        "term_a": "Kashi",
        "term_b": "Varanasi",
        "distinction": "Kashi is the ancient sacred name of the city meaning City of Light in Sanskrit. Varanasi is the modern official name derived from the rivers Varuna and Asi that border the city. They refer to the same city but carry different connotations.",
        "stakes": "low",
        "correct_context": "Kashi is used in religious and spiritual contexts. Varanasi is used in administrative and geographic contexts.",
        "confusion_probe": "The ancient Sanskrit name for the holy city on the banks of the Ganges meaning City of Light is what?",
        "correct_answer": "Kashi",
        "confused_answer": "Varanasi"
    },
    {
        "id": "cul_024",
        "term_a": "Bodhi tree",
        "term_b": "Ashoka tree",
        "distinction": "The Bodhi tree is the sacred fig tree under which Gautama Buddha attained enlightenment at Bodh Gaya. The Ashoka tree is a tree sacred in Hindu and Buddhist traditions associated with the Mauryan emperor Ashoka.",
        "stakes": "medium",
        "correct_context": "The fig tree under which Buddha sat to attain enlightenment is the Bodhi tree. The flowering tree planted at Buddhist sites by Emperor Ashoka is the Ashoka tree.",
        "confusion_probe": "The sacred fig tree under which Gautama Buddha attained enlightenment at Bodh Gaya is called what?",
        "correct_answer": "Bodhi tree",
        "confused_answer": "Ashoka tree"
    },
    {
        "id": "cul_025",
        "term_a": "warp",
        "term_b": "weft",
        "distinction": "In weaving, the warp is the set of threads stretched lengthwise on the loom. The weft is the thread woven horizontally across the warp threads. Both are essential to Banarasi silk weaving.",
        "stakes": "low",
        "correct_context": "The vertical threads on the loom that the weaver stretches before beginning are the warp. The horizontal thread passed through the warp to create the fabric pattern is the weft.",
        "confusion_probe": "In Banarasi silk weaving, the horizontal thread that is passed back and forth through the vertical loom threads to create the brocade pattern is called what?",
        "correct_answer": "weft",
        "confused_answer": "warp"
    }
]

ADDITIONAL_EMERGENCY = [
    {
        "id": "emr_004",
        "term_a": "triage",
        "term_b": "diagnosis",
        "distinction": "Triage is the rapid sorting of patients by urgency to determine the order of treatment. Diagnosis is the identification of a specific disease or condition.",
        "stakes": "high",
        "correct_context": "Quickly sorting mass casualty victims into immediate, delayed, and expectant categories at an accident site is triage. Identifying that a patient has a ruptured spleen is diagnosis.",
        "confusion_probe": "At a mass casualty event, medical personnel quickly sort victims into categories based on injury severity to determine who gets treated first. What process is this?",
        "correct_answer": "triage",
        "confused_answer": "diagnosis"
    },
    {
        "id": "emr_005",
        "term_a": "blood type compatibility",
        "term_b": "cross-matching",
        "distinction": "Blood type compatibility is the general matching of ABO and Rh blood groups between donor and recipient. Cross-matching is a specific laboratory test that mixes donor blood with recipient blood to check for adverse reactions before transfusion.",
        "stakes": "high",
        "correct_context": "Knowing a patient is O-positive and selecting O-positive or O-negative blood is blood type compatibility. Running a lab test mixing the selected donor blood with the patient's blood before transfusing is cross-matching.",
        "confusion_probe": "A laboratory test that physically mixes a donor blood sample with a recipient blood sample to detect any incompatibility reactions before transfusion is called what?",
        "correct_answer": "cross-matching",
        "confused_answer": "blood type compatibility"
    },
    {
        "id": "emr_006",
        "term_a": "whole blood",
        "term_b": "packed red blood cells",
        "distinction": "Whole blood contains all blood components — red cells, white cells, platelets, and plasma. Packed red blood cells are whole blood with plasma and most platelets removed, used specifically for anaemia and blood loss.",
        "stakes": "high",
        "correct_context": "Blood donated directly and transfused without separation is whole blood. Blood processed to remove plasma and concentrate red cells for an anaemic patient is packed red blood cells.",
        "confusion_probe": "A patient with severe anaemia due to blood loss needs a transfusion of red cells with plasma removed to increase oxygen-carrying capacity. What blood product is this?",
        "correct_answer": "packed red blood cells",
        "confused_answer": "whole blood"
    },
    {
        "id": "emr_007",
        "term_a": "universal donor",
        "term_b": "universal recipient",
        "distinction": "Universal donor is blood type O-negative — can donate red blood cells to any blood type. Universal recipient is blood type AB-positive — can receive red blood cells from any blood type.",
        "stakes": "high",
        "correct_context": "O-negative blood given to an unknown patient in emergency is universal donor blood. An AB-positive patient who can receive any blood type is a universal recipient.",
        "confusion_probe": "In emergency situations where a patient's blood type is unknown, blood type O-negative is used because it is compatible with all blood types. O-negative is called what?",
        "correct_answer": "universal donor",
        "confused_answer": "universal recipient"
    },
    {
        "id": "emr_008",
        "term_a": "blood bank",
        "term_b": "blood centre",
        "distinction": "A blood bank is a hospital-based facility that stores and dispenses blood for that hospital's patients. A blood centre is a standalone regional facility that collects, processes, and distributes blood to multiple hospitals.",
        "stakes": "medium",
        "correct_context": "The storage unit within a hospital that keeps blood for surgical patients is a blood bank. The regional facility that collects donations and supplies multiple hospitals is a blood centre.",
        "confusion_probe": "A facility within a hospital that stores blood products specifically for that hospital's surgical and emergency patients is called what?",
        "correct_answer": "blood bank",
        "confused_answer": "blood centre"
    },
    {
        "id": "emr_009",
        "term_a": "voluntary donation",
        "term_b": "directed donation",
        "distinction": "Voluntary donation is blood given altruistically to a general blood supply without specifying a recipient. Directed donation is blood given by a donor specifically for a named patient.",
        "stakes": "medium",
        "correct_context": "A person donating blood at a blood drive with no specific patient in mind is voluntary donation. A father donating blood specifically for his child's upcoming surgery is directed donation.",
        "confusion_probe": "A person donates blood at a community blood drive with no specific recipient in mind and the blood enters the general supply. What type of donation is this?",
        "correct_answer": "voluntary donation",
        "confused_answer": "directed donation"
    },
    {
        "id": "emr_010",
        "term_a": "haemorrhage",
        "term_b": "haematoma",
        "distinction": "Haemorrhage is active bleeding — blood escaping from blood vessels either internally or externally. Haematoma is a localised collection of blood that has already escaped and pooled in tissue.",
        "stakes": "high",
        "correct_context": "Blood actively flowing from a ruptured artery is haemorrhage. A pocket of clotted blood collected under the skull after head trauma is a haematoma.",
        "confusion_probe": "A patient with a ruptured spleen has blood actively escaping into the abdominal cavity. What is this called?",
        "correct_answer": "haemorrhage",
        "confused_answer": "haematoma"
    },
    {
        "id": "emr_011",
        "term_a": "resuscitation",
        "term_b": "stabilisation",
        "distinction": "Resuscitation is the emergency restoration of vital functions in a patient who has lost them. Stabilisation is the process of bringing a patient's condition under control after resuscitation to prevent further deterioration.",
        "stakes": "high",
        "correct_context": "Performing CPR to restart a stopped heart is resuscitation. Administering fluids and monitoring a post-cardiac arrest patient to maintain stable vitals is stabilisation.",
        "confusion_probe": "A patient whose heart has stopped receives CPR and defibrillation to restore heartbeat and breathing. This emergency restoration of vital functions is called what?",
        "correct_answer": "resuscitation",
        "confused_answer": "stabilisation"
    },
    {
        "id": "emr_012",
        "term_a": "plasma",
        "term_b": "serum",
        "distinction": "Plasma is the liquid component of blood containing clotting factors. Serum is plasma with clotting factors removed — what remains after blood has clotted.",
        "stakes": "high",
        "correct_context": "The yellow liquid separated from blood cells that still contains fibrinogen is plasma. The liquid remaining after blood clots and clotting factors are consumed is serum.",
        "confusion_probe": "The liquid component of blood that contains clotting factors and is used in fresh frozen plasma transfusions is called what?",
        "correct_answer": "plasma",
        "confused_answer": "serum"
    },
    {
        "id": "emr_013",
        "term_a": "token reservation",
        "term_b": "direct allocation",
        "distinction": "Token reservation locks a blood unit for a specific patient in transit preventing concurrent reallocation. Direct allocation immediately assigns blood to the nearest available patient without a reservation lock.",
        "stakes": "high",
        "correct_context": "Locking a specific O-negative unit for a patient in transit to prevent it being given to another patient is token reservation. Immediately giving the nearest available O-negative unit to the first requesting patient is direct allocation.",
        "confusion_probe": "In a blood bank management system, the mechanism that locks a specific blood unit for a requesting patient while they are en route to prevent it being reallocated is called what?",
        "correct_answer": "token reservation",
        "confused_answer": "direct allocation"
    },
    {
        "id": "emr_014",
        "term_a": "spatial clustering",
        "term_b": "priority scoring",
        "distinction": "Spatial clustering groups blood banks by geographic proximity using algorithms like K-means. Priority scoring ranks patients by medical urgency, blood type compatibility, and distance to determine allocation order.",
        "stakes": "medium",
        "correct_context": "Grouping blood banks within 10km of a hospital using K-means on GPS coordinates is spatial clustering. Ranking a trauma patient above a scheduled surgery patient because of urgency score is priority scoring.",
        "confusion_probe": "The process of ranking patients by medical urgency, blood type match, and distance to determine who receives scarce blood units first is called what?",
        "correct_answer": "priority scoring",
        "confused_answer": "spatial clustering"
    },
    {
        "id": "emr_015",
        "term_a": "blood group",
        "term_b": "Rh factor",
        "distinction": "Blood group refers to the ABO classification — A, B, AB, or O. Rh factor is a separate antigen classification — positive or negative. Together they form the complete blood type.",
        "stakes": "high",
        "correct_context": "Whether a patient is type A, B, AB, or O is their blood group. Whether they are positive or negative based on the Rh antigen is their Rh factor.",
        "confusion_probe": "The classification of blood as A, B, AB, or O based on antigens on red blood cell surfaces is called what?",
        "correct_answer": "blood group",
        "confused_answer": "Rh factor"
    },
    {
        "id": "emr_016",
        "term_a": "expiry",
        "term_b": "contamination",
        "distinction": "Blood expiry is when a blood unit reaches the end of its safe storage period and can no longer be used. Contamination is when a blood unit becomes infected with bacteria, viruses, or other pathogens during collection or storage.",
        "stakes": "high",
        "correct_context": "Red blood cells stored for more than 42 days have expired. Red blood cells infected with bacteria during collection are contaminated.",
        "confusion_probe": "A blood unit that has been stored beyond its 42-day maximum storage period and can no longer be safely transfused has reached what state?",
        "correct_answer": "expiry",
        "confused_answer": "contamination"
    },
    {
        "id": "emr_017",
        "term_a": "mass casualty incident",
        "term_b": "disaster",
        "distinction": "A mass casualty incident is a specific event producing more patients than local resources can handle. A disaster is a broader term for any event causing widespread damage, loss, or distress — not necessarily medical.",
        "stakes": "high",
        "correct_context": "A train derailment producing 200 injured patients overwhelming 3 hospitals is a mass casualty incident. A flood destroying a city's infrastructure and displacing thousands is a disaster.",
        "confusion_probe": "A building collapse produces 150 injured victims overwhelming the capacity of all nearby hospitals. What specific emergency medical term describes this situation?",
        "correct_answer": "mass casualty incident",
        "confused_answer": "disaster"
    }
]

data["medical"].extend(ADDITIONAL_MEDICAL)
data["cultural_heritage"].extend(ADDITIONAL_CULTURAL)
data["emergency_resource"].extend(ADDITIONAL_EMERGENCY)

with open("data/concept_pairs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = (
    len(data["medical"]) +
    len(data["cultural_heritage"]) +
    len(data["emergency_resource"])
)

print("Dataset expanded successfully.")
print(f"Medical pairs: {len(data['medical'])}")
print(f"Cultural heritage pairs: {len(data['cultural_heritage'])}")
print(f"Emergency resource pairs: {len(data['emergency_resource'])}")
print(f"Total pairs: {total}")