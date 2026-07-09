import json
import os

ALL_PAIRS = {
    "medical": [
        {
            "id": "med_001",
            "term_a": "cardiac arrest",
            "term_b": "heart attack",
            "distinction": "Cardiac arrest is the sudden stoppage of heart function — the heart stops beating. Heart attack (myocardial infarction) is a blockage of blood supply to the heart muscle. A heart attack can cause cardiac arrest but they are distinct conditions.",
            "stakes": "high",
            "correct_context": "A patient with no pulse and not breathing is in cardiac arrest. A patient with chest pain and blocked arteries is having a heart attack.",
            "confusion_probe": "A patient suddenly collapses, has no pulse, and is not breathing. What medical emergency is this?",
            "correct_answer": "cardiac arrest",
            "confused_answer": "heart attack"
        },
        {
            "id": "med_002",
            "term_a": "hypoglycemia",
            "term_b": "hypotension",
            "distinction": "Hypoglycemia is abnormally low blood sugar. Hypotension is abnormally low blood pressure. Both cause dizziness and weakness but require completely different interventions.",
            "stakes": "high",
            "correct_context": "A diabetic patient who has not eaten feels dizzy and shaky — hypoglycemia. A patient who feels faint when standing up has low blood pressure — hypotension.",
            "confusion_probe": "A diabetic patient who skipped meals is dizzy, shaky, and sweating. What condition are they experiencing?",
            "correct_answer": "hypoglycemia",
            "confused_answer": "hypotension"
        },
        {
            "id": "med_003",
            "term_a": "stroke",
            "term_b": "transient ischaemic attack",
            "distinction": "A stroke causes permanent brain damage due to blocked or burst blood vessel. A TIA is a temporary blockage that resolves within 24 hours with no permanent damage. TIA is a warning sign for stroke.",
            "stakes": "high",
            "correct_context": "Symptoms lasting more than 24 hours with permanent deficit indicate stroke. Symptoms resolving completely within hours indicate TIA.",
            "confusion_probe": "A patient had sudden weakness on one side of the body that completely resolved within 2 hours. What is this called?",
            "correct_answer": "transient ischaemic attack",
            "confused_answer": "stroke"
        },
        {
            "id": "med_004",
            "term_a": "sepsis",
            "term_b": "infection",
            "distinction": "Infection is the presence of a pathogen in the body. Sepsis is the life-threatening systemic inflammatory response to infection — the immune system overreacts and begins damaging the body itself.",
            "stakes": "high",
            "correct_context": "A patient with a wound and localised redness has an infection. A patient with fever, rapid heart rate, confusion, and organ dysfunction from an infection has sepsis.",
            "confusion_probe": "A patient with a urinary tract infection develops high fever, confusion, and their blood pressure drops dangerously. What has this progressed to?",
            "correct_answer": "sepsis",
            "confused_answer": "infection"
        },
        {
            "id": "med_005",
            "term_a": "fracture",
            "term_b": "sprain",
            "distinction": "A fracture is a break in a bone. A sprain is a tear or stretch of a ligament connecting bones. Both cause pain and swelling but require different treatment.",
            "stakes": "medium",
            "correct_context": "Bone broken after impact is a fracture. Twisted ankle with ligament damage is a sprain.",
            "confusion_probe": "An athlete twists their ankle and an X-ray shows no bone damage but there is ligament tearing. What is this injury?",
            "correct_answer": "sprain",
            "confused_answer": "fracture"
        },
        {
            "id": "med_006",
            "term_a": "dementia",
            "term_b": "delirium",
            "distinction": "Dementia is a chronic progressive decline in cognitive function. Delirium is an acute sudden confused state often caused by illness, medication, or infection — it is reversible.",
            "stakes": "high",
            "correct_context": "Gradual memory loss over years in an elderly patient is dementia. Sudden onset confusion in a hospitalised patient that resolves when infection is treated is delirium.",
            "confusion_probe": "An 80-year-old hospitalised patient suddenly becomes confused and agitated overnight. Tests show a urinary tract infection. What is this acute condition called?",
            "correct_answer": "delirium",
            "confused_answer": "dementia"
        },
        {
            "id": "med_007",
            "term_a": "anaphylaxis",
            "term_b": "allergy",
            "distinction": "An allergy is an immune response to a foreign substance causing localised symptoms. Anaphylaxis is a severe life-threatening systemic allergic reaction requiring immediate epinephrine.",
            "stakes": "high",
            "correct_context": "Runny nose after eating peanuts is an allergy. Throat swelling, difficulty breathing, and blood pressure drop after eating peanuts is anaphylaxis.",
            "confusion_probe": "A patient who ate peanuts develops throat swelling, cannot breathe properly, and their blood pressure drops rapidly. What emergency is this?",
            "correct_answer": "anaphylaxis",
            "confused_answer": "allergy"
        },
        {
            "id": "med_008",
            "term_a": "psychosis",
            "term_b": "neurosis",
            "distinction": "Psychosis involves a break from reality — hallucinations, delusions. Neurosis involves distressing but reality-based anxiety disorders. A psychotic patient does not know they are ill. A neurotic patient does.",
            "stakes": "high",
            "correct_context": "Patient hearing voices that are not there and believing they are being followed — psychosis. Patient with excessive anxiety about germs who knows the fear is irrational — neurosis.",
            "confusion_probe": "A patient believes that the government is inserting thoughts into their mind and hears voices commanding them. What condition is this?",
            "correct_answer": "psychosis",
            "confused_answer": "neurosis"
        },
        {
            "id": "med_009",
            "term_a": "epidemic",
            "term_b": "pandemic",
            "distinction": "An epidemic is an outbreak of disease spreading rapidly within a community or region. A pandemic is an epidemic that has spread across multiple countries or continents.",
            "stakes": "medium",
            "correct_context": "Dengue spreading rapidly across one Indian state is an epidemic. COVID-19 spreading across every continent is a pandemic.",
            "confusion_probe": "A disease is spreading rapidly but is confined to three districts of one state. What is the correct term for this outbreak?",
            "correct_answer": "epidemic",
            "confused_answer": "pandemic"
        },
        {
            "id": "med_010",
            "term_a": "palliative care",
            "term_b": "hospice care",
            "distinction": "Palliative care focuses on comfort and quality of life for any serious illness at any stage — patients may still be receiving curative treatment. Hospice care is specifically for patients in the final months of life who have stopped curative treatment.",
            "stakes": "high",
            "correct_context": "A cancer patient receiving chemotherapy but also getting pain management is receiving palliative care. A terminal patient who has stopped all curative treatment is in hospice care.",
            "confusion_probe": "A patient with stage 4 cancer is still undergoing chemotherapy but receiving pain and symptom management. What type of care is the symptom management called?",
            "correct_answer": "palliative care",
            "confused_answer": "hospice care"
        },
        {
            "id": "med_011",
            "term_a": "type 1 diabetes",
            "term_b": "type 2 diabetes",
            "distinction": "Type 1 diabetes is an autoimmune condition where the pancreas produces no insulin. Type 2 diabetes is a metabolic condition where the body becomes resistant to insulin.",
            "stakes": "high",
            "correct_context": "A child diagnosed with diabetes whose pancreas produces zero insulin has type 1. An overweight adult whose cells stop responding to insulin has type 2.",
            "confusion_probe": "A 10-year-old child is diagnosed with diabetes and told their pancreas produces no insulin at all. What type of diabetes is this?",
            "correct_answer": "type 1 diabetes",
            "confused_answer": "type 2 diabetes"
        },
        {
            "id": "med_012",
            "term_a": "tachycardia",
            "term_b": "bradycardia",
            "distinction": "Tachycardia is an abnormally fast heart rate above 100 beats per minute. Bradycardia is an abnormally slow heart rate below 60 beats per minute.",
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
            "distinction": "A benign tumor is non-cancerous and does not spread. A malignant tumor is cancerous, invades surrounding tissue, and can metastasize.",
            "stakes": "high",
            "correct_context": "A slow-growing encapsulated lump that stays in one place is benign. A tumor that invades muscle and spreads to lymph nodes is malignant.",
            "confusion_probe": "A tumor found in a patient's breast is encapsulated and shows no signs of spreading. What type of tumor is this?",
            "correct_answer": "benign tumor",
            "confused_answer": "malignant tumor"
        },
        {
            "id": "med_014",
            "term_a": "acute pain",
            "term_b": "chronic pain",
            "distinction": "Acute pain is short-term pain that arises suddenly and resolves as healing occurs. Chronic pain persists for more than 3 months.",
            "stakes": "medium",
            "correct_context": "Pain immediately after surgery that resolves over weeks is acute. Pain persisting for years after an injury is chronic.",
            "confusion_probe": "A patient who broke their arm 2 weeks ago is experiencing pain that is gradually improving. What type of pain is this?",
            "correct_answer": "acute pain",
            "confused_answer": "chronic pain"
        },
        {
            "id": "med_015",
            "term_a": "arteries",
            "term_b": "veins",
            "distinction": "Arteries carry oxygenated blood away from the heart. Veins carry deoxygenated blood back to the heart.",
            "stakes": "high",
            "correct_context": "The aorta carries oxygen-rich blood from the heart — it is an artery. The vena cava returns oxygen-depleted blood — it is a vein.",
            "confusion_probe": "The blood vessels that carry oxygenated blood away from the heart to supply organs are called what?",
            "correct_answer": "arteries",
            "confused_answer": "veins"
        },
        {
            "id": "med_016",
            "term_a": "antibiotic",
            "term_b": "antiviral",
            "distinction": "Antibiotics treat bacterial infections. Antivirals treat viral infections. Antibiotics have no effect on viruses.",
            "stakes": "high",
            "correct_context": "Amoxicillin for bacterial pneumonia is an antibiotic. Oseltamivir for influenza is an antiviral.",
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
            "correct_context": "A person who cannot get measles has immunity. The act of giving a measles vaccine is immunisation.",
            "confusion_probe": "The process of administering a vaccine to a child to protect them against polio is called what?",
            "correct_answer": "immunisation",
            "confused_answer": "immunity"
        },
        {
            "id": "med_018",
            "term_a": "sign",
            "term_b": "symptom",
            "distinction": "A symptom is what the patient reports — subjective. A sign is what a clinician observes or measures — objective.",
            "stakes": "medium",
            "correct_context": "A patient saying they feel hot is a symptom. A doctor measuring 39 degrees Celsius is a sign.",
            "confusion_probe": "A doctor measures a patient's blood pressure at 180/110 mmHg. This observed measurement is called what?",
            "correct_answer": "sign",
            "confused_answer": "symptom"
        },
        {
            "id": "med_019",
            "term_a": "prognosis",
            "term_b": "diagnosis",
            "distinction": "Diagnosis is the identification of a disease. Prognosis is the predicted outcome of that condition.",
            "stakes": "medium",
            "correct_context": "Identifying stage 3 lung cancer is the diagnosis. Estimating 18-month survival probability is the prognosis.",
            "confusion_probe": "After running tests, a doctor tells a patient they have type 2 diabetes. This identification is called what?",
            "correct_answer": "diagnosis",
            "confused_answer": "prognosis"
        },
        {
            "id": "med_020",
            "term_a": "contraindication",
            "term_b": "side effect",
            "distinction": "A contraindication is a condition making a treatment unsafe. A side effect is an unintended effect alongside the therapeutic effect.",
            "stakes": "high",
            "correct_context": "Aspirin being unsafe for bleeding disorder patients is a contraindication. Aspirin causing stomach irritation is a side effect.",
            "confusion_probe": "A patient taking ibuprofen develops stomach irritation as an unintended result. This is called what?",
            "correct_answer": "side effect",
            "confused_answer": "contraindication"
        },
        {
            "id": "med_021",
            "term_a": "incidence",
            "term_b": "prevalence",
            "distinction": "Incidence is the number of new cases over a time period. Prevalence is the total existing cases at a given point.",
            "stakes": "medium",
            "correct_context": "1000 new diabetes diagnoses in 2025 is incidence. 77 million people currently living with diabetes is prevalence.",
            "confusion_probe": "500 new tuberculosis cases diagnosed in a city during 2025. This figure represents what measure?",
            "correct_answer": "incidence",
            "confused_answer": "prevalence"
        },
        {
            "id": "med_022",
            "term_a": "hematoma",
            "term_b": "edema",
            "distinction": "A hematoma is a localised collection of blood outside vessels. Edema is swelling from excess fluid in tissue.",
            "stakes": "medium",
            "correct_context": "Pooled blood under skin after head injury is a hematoma. Swollen ankles from fluid buildup in heart failure is edema.",
            "confusion_probe": "After a head injury, a patient develops a localised blood collection beneath the skull. What is this called?",
            "correct_answer": "hematoma",
            "confused_answer": "edema"
        },
        {
            "id": "med_023",
            "term_a": "dialysis",
            "term_b": "transplant",
            "distinction": "Dialysis artificially performs kidney filtration. Transplant is surgical replacement of a failed organ.",
            "stakes": "high",
            "correct_context": "A patient attached to a filtration machine three times weekly is on dialysis. A patient receiving a new kidney undergoes transplant.",
            "confusion_probe": "A patient with kidney failure has blood filtered by a machine three times a week. What procedure is this?",
            "correct_answer": "dialysis",
            "confused_answer": "transplant"
        },
        {
            "id": "med_024",
            "term_a": "prophylaxis",
            "term_b": "treatment",
            "distinction": "Prophylaxis is preventive action before disease occurs. Treatment is intervention after a condition develops.",
            "stakes": "high",
            "correct_context": "Taking malaria medication before travel is prophylaxis. Taking it after diagnosis is treatment.",
            "confusion_probe": "A traveller takes antimalarial medication before visiting an endemic country to prevent infection. This is called what?",
            "correct_answer": "prophylaxis",
            "confused_answer": "treatment"
        },
        {
            "id": "med_025",
            "term_a": "acute kidney injury",
            "term_b": "chronic kidney disease",
            "distinction": "Acute kidney injury is sudden rapid kidney failure, often reversible. Chronic kidney disease is gradual progressive loss over months to years, generally irreversible.",
            "stakes": "high",
            "correct_context": "Kidneys failing after severe infection that recover after treatment — acute kidney injury. Kidney function declining over 5 years in a diabetic — chronic kidney disease.",
            "confusion_probe": "A patient develops sudden kidney failure within 48 hours of a severe infection. Kidneys may recover. What is this called?",
            "correct_answer": "acute kidney injury",
            "confused_answer": "chronic kidney disease"
        },
        {
            "id": "med_041",
            "term_a": "coma",
            "term_b": "vegetative state",
            "distinction": "Coma is complete unconsciousness with no sleep-wake cycles. Vegetative state has sleep-wake cycles and basic reflexes but no awareness.",
            "stakes": "high",
            "correct_context": "No response to any stimulus with no sleep-wake cycle is coma. Eyes open spontaneously with no awareness is vegetative state.",
            "confusion_probe": "A patient opens their eyes spontaneously and has sleep-wake cycles but shows no awareness. What condition is this?",
            "correct_answer": "vegetative state",
            "confused_answer": "coma"
        },
        {
            "id": "med_042",
            "term_a": "pandemic",
            "term_b": "endemic",
            "distinction": "A pandemic spreads globally. An endemic disease is constantly present at baseline in a specific region.",
            "stakes": "medium",
            "correct_context": "COVID-19 spreading across every continent is a pandemic. Malaria consistently present in sub-Saharan Africa is endemic.",
            "confusion_probe": "Malaria is consistently present at predictable levels in certain regions of India year after year. What term describes this?",
            "correct_answer": "endemic",
            "confused_answer": "pandemic"
        },
        {
            "id": "med_043",
            "term_a": "intubation",
            "term_b": "ventilation",
            "distinction": "Intubation is inserting a tube into the trachea to maintain airway. Ventilation is mechanically moving air into and out of lungs.",
            "stakes": "high",
            "correct_context": "Inserting a breathing tube is intubation. The machine pushing air into lungs is ventilation.",
            "confusion_probe": "The procedure of inserting a tube through a patient's mouth into the trachea to secure the airway is called what?",
            "correct_answer": "intubation",
            "confused_answer": "ventilation"
        }
    ],
    "cultural_heritage": [
        {
            "id": "cul_001",
            "term_a": "moksha",
            "term_b": "nirvana",
            "distinction": "Moksha is the Hindu concept of liberation — union with Brahman. Nirvana is the Buddhist concept — extinguishing desire and suffering. Different philosophical frameworks.",
            "stakes": "medium",
            "correct_context": "A Hindu seeking union with the universal soul seeks moksha. A Buddhist seeking end of suffering seeks nirvana.",
            "confusion_probe": "In Hindu philosophy, the final liberation of the soul from the cycle of rebirth and union with Brahman is called what?",
            "correct_answer": "moksha",
            "confused_answer": "nirvana"
        },
        {
            "id": "cul_002",
            "term_a": "aarti",
            "term_b": "puja",
            "distinction": "Puja is the broad Hindu worship ritual. Aarti is a specific component — waving lit lamps before the deity with devotional songs.",
            "stakes": "low",
            "correct_context": "The entire worship ceremony is puja. The specific lamp-waving with hymns is aarti.",
            "confusion_probe": "A priest waves a lit lamp in circular motions before the deity while devotees sing hymns. What is this specific ritual?",
            "correct_answer": "aarti",
            "confused_answer": "puja"
        },
        {
            "id": "cul_003",
            "term_a": "raga",
            "term_b": "tala",
            "distinction": "Raga is the melodic framework — notes and emotional character. Tala is the rhythmic cycle of beats.",
            "stakes": "medium",
            "correct_context": "The scale of notes and emotional mood is the raga. The rhythmic pattern of beats is the tala.",
            "confusion_probe": "In Hindustani classical music, the melodic framework specifying which notes to use and their emotional character is called what?",
            "correct_answer": "raga",
            "confused_answer": "tala"
        },
        {
            "id": "cul_004",
            "term_a": "stupa",
            "term_b": "temple",
            "distinction": "A stupa is a Buddhist dome-shaped monument for circumambulation. A temple is an active place of worship housing a deity.",
            "stakes": "medium",
            "correct_context": "The Dhamek Stupa at Sarnath is a Buddhist monument. Kashi Vishwanath is an active Hindu temple.",
            "confusion_probe": "The dome-shaped Buddhist monument at Sarnath containing sacred relics around which pilgrims walk is called what?",
            "correct_answer": "stupa",
            "confused_answer": "temple"
        },
        {
            "id": "cul_005",
            "term_a": "ghat",
            "term_b": "kund",
            "distinction": "A ghat is steps leading to a river for bathing or rituals. A kund is a sacred enclosed tank or pool for ritual bathing.",
            "stakes": "low",
            "correct_context": "The stepped riverfront along the Ganges are ghats. A sacred enclosed water tank at a temple is a kund.",
            "confusion_probe": "The stepped stone staircases descending to the Ganges where Hindus perform ritual bathing are called what?",
            "correct_answer": "ghat",
            "confused_answer": "kund"
        },
        {
            "id": "cul_006",
            "term_a": "dharma",
            "term_b": "karma",
            "distinction": "Dharma is one's duty and moral order. Karma is the law of cause and effect across lifetimes.",
            "stakes": "medium",
            "correct_context": "A warrior fulfilling duty to protect follows dharma. Good fortune from past good deeds is karma.",
            "confusion_probe": "In Hindu philosophy, the term for one's sacred duty according to their station in life is called what?",
            "correct_answer": "dharma",
            "confused_answer": "karma"
        },
        {
            "id": "cul_007",
            "term_a": "gharana",
            "term_b": "sampradaya",
            "distinction": "Gharana is a hereditary school of classical music. Sampradaya is a broader religious or philosophical tradition.",
            "stakes": "medium",
            "correct_context": "The Benares gharana is a tabla lineage. A sampradaya is a religious sect with its own philosophy.",
            "confusion_probe": "The hereditary school of tabla playing originating in Varanasi with a distinctive open style is called what?",
            "correct_answer": "gharana",
            "confused_answer": "sampradaya"
        },
        {
            "id": "cul_008",
            "term_a": "Sanskrit",
            "term_b": "Pali",
            "distinction": "Sanskrit is the classical language of Hinduism. Pali is the classical language of Theravada Buddhism.",
            "stakes": "medium",
            "correct_context": "The Vedas are in Sanskrit. The Tripitaka is in Pali.",
            "confusion_probe": "The language in which the Hindu Vedas and Upanishads were composed is called what?",
            "correct_answer": "Sanskrit",
            "confused_answer": "Pali"
        },
        {
            "id": "cul_009",
            "term_a": "zari",
            "term_b": "zardozi",
            "distinction": "Zari is the metallic thread itself. Zardozi is the embroidery technique using zari thread.",
            "stakes": "low",
            "correct_context": "The gold thread in Banarasi silk is zari. The raised gold embroidery technique is zardozi.",
            "confusion_probe": "The metallic gold or silver thread woven into Banarasi silk sarees is called what?",
            "correct_answer": "zari",
            "confused_answer": "zardozi"
        },
        {
            "id": "cul_010",
            "term_a": "cremation",
            "term_b": "immersion",
            "distinction": "Cremation is burning the body after death. Immersion is ritual submersion of ashes or idols in a sacred river.",
            "stakes": "medium",
            "correct_context": "Burning a body at Manikarnika Ghat is cremation. Immersing Ganesh idols after the festival is immersion.",
            "confusion_probe": "The ritual burning of a deceased Hindu at Manikarnika Ghat in Varanasi is called what?",
            "correct_answer": "cremation",
            "confused_answer": "immersion"
        },
        {
            "id": "cul_011",
            "term_a": "Vedas",
            "term_b": "Upanishads",
            "distinction": "The Vedas are the oldest sacred Hindu texts with hymns and rituals. The Upanishads are later philosophical texts exploring reality and the self.",
            "stakes": "medium",
            "correct_context": "The Rigveda with hymns is a Veda. The Brihadaranyaka Upanishad exploring Brahman is an Upanishad.",
            "confusion_probe": "The ancient Hindu philosophical texts exploring the nature of the self forming the concluding portion of the Vedic corpus are called what?",
            "correct_answer": "Upanishads",
            "confused_answer": "Vedas"
        },
        {
            "id": "cul_012",
            "term_a": "pilgrimage",
            "term_b": "tourism",
            "distinction": "Pilgrimage is travel to a sacred place for religious purposes. Tourism is travel for leisure without religious motivation.",
            "stakes": "low",
            "correct_context": "Travelling to Varanasi for spiritual bathing is pilgrimage. Travelling to photograph the ghats is tourism.",
            "confusion_probe": "A devout Hindu travels to Varanasi specifically to perform ritual bathing in the Ganges for spiritual merit. What type of journey is this?",
            "correct_answer": "pilgrimage",
            "confused_answer": "tourism"
        },
        {
            "id": "cul_013",
            "term_a": "tabla",
            "term_b": "mridangam",
            "distinction": "Tabla is a pair of hand drums in Hindustani music of North India. Mridangam is a double-headed drum in Carnatic music of South India.",
            "stakes": "medium",
            "correct_context": "The percussion in a sitar recital in Varanasi is tabla. The percussion in a veena recital in Chennai is mridangam.",
            "confusion_probe": "The pair of hand drums accompanying Hindustani classical music in North India is called what?",
            "correct_answer": "tabla",
            "confused_answer": "mridangam"
        },
        {
            "id": "cul_014",
            "term_a": "Katan silk",
            "term_b": "Georgette",
            "distinction": "Katan silk is pure silk woven from raw threads for traditional Banarasi sarees. Georgette is lightweight crinkled fabric in a different Banarasi variety.",
            "stakes": "low",
            "correct_context": "The heaviest traditional Banarasi saree from pure raw silk is Katan. The lighter crinkled variety is Georgette.",
            "confusion_probe": "The traditional Banarasi saree woven from pure raw silk producing a heavy lustrous fabric is called what variety?",
            "correct_answer": "Katan silk",
            "confused_answer": "Georgette"
        },
        {
            "id": "cul_015",
            "term_a": "Hindustani music",
            "term_b": "Carnatic music",
            "distinction": "Hindustani music is North Indian classical music influenced by Persian and Mughal traditions. Carnatic music is South Indian classical music with Vedic roots.",
            "stakes": "medium",
            "correct_context": "The classical music of Varanasi is Hindustani. The classical music of Chennai is Carnatic.",
            "confusion_probe": "The classical music tradition of Varanasi influenced by Mughal court culture is called what?",
            "correct_answer": "Hindustani music",
            "confused_answer": "Carnatic music"
        },
        {
            "id": "cul_016",
            "term_a": "mantra",
            "term_b": "shloka",
            "distinction": "A mantra is a sacred sound repeated for spiritual power. A shloka is a verse from Hindu scriptures in a specific poetic meter.",
            "stakes": "low",
            "correct_context": "Om Namah Shivaya chanted in meditation is a mantra. A Bhagavad Gita verse in anushtubh meter is a shloka.",
            "confusion_probe": "Om Namah Shivaya repeatedly chanted during Shiva worship for spiritual power is called what?",
            "correct_answer": "mantra",
            "confused_answer": "shloka"
        },
        {
            "id": "cul_017",
            "term_a": "avatar",
            "term_b": "deity",
            "distinction": "A deity is a divine being worshipped as a god. An avatar is a specific earthly incarnation of a deity.",
            "stakes": "medium",
            "correct_context": "Vishnu is a deity. Rama and Krishna are avatars of Vishnu.",
            "confusion_probe": "Krishna, considered an earthly incarnation of Vishnu, is what type of divine manifestation?",
            "correct_answer": "avatar",
            "confused_answer": "deity"
        },
        {
            "id": "cul_018",
            "term_a": "ashram",
            "term_b": "monastery",
            "distinction": "An ashram is a Hindu spiritual community under a guru. A monastery is a Buddhist or Christian institution for monks.",
            "stakes": "low",
            "correct_context": "A Hindu community with a guru for spiritual learning is an ashram. A Buddhist institution for monks is a monastery.",
            "confusion_probe": "A community in Varanasi where Hindu disciples live with a spiritual teacher to practice yoga is called what?",
            "correct_answer": "ashram",
            "confused_answer": "monastery"
        },
        {
            "id": "cul_019",
            "term_a": "prasad",
            "term_b": "bhog",
            "distinction": "Bhog is food offered to a deity during worship. Prasad is the same food after being blessed and distributed to devotees.",
            "stakes": "low",
            "correct_context": "Sweets placed before the deity are bhog. Sweets distributed to devotees after the offering are prasad.",
            "confusion_probe": "Food offered to a Hindu deity then distributed to devotees as a blessed gift is called what?",
            "correct_answer": "prasad",
            "confused_answer": "bhog"
        },
        {
            "id": "cul_020",
            "term_a": "Ramcharitmanas",
            "term_b": "Ramayana",
            "distinction": "The Ramayana is the ancient Sanskrit epic by Valmiki. The Ramcharitmanas is a 16th century Awadhi retelling by Tulsidas.",
            "stakes": "medium",
            "correct_context": "The original Sanskrit epic by Valmiki is the Ramayana. The Awadhi version by Tulsidas at the Tulsi Manas Mandir is the Ramcharitmanas.",
            "confusion_probe": "The 16th century Awadhi language retelling of the Rama story by Tulsidas is called what?",
            "correct_answer": "Ramcharitmanas",
            "confused_answer": "Ramayana"
        },
        {
            "id": "cul_021",
            "term_a": "cremation ground",
            "term_b": "burial ground",
            "distinction": "A cremation ground is where Hindu bodies are burned. A burial ground is where bodies are interred in earth.",
            "stakes": "medium",
            "correct_context": "Manikarnika Ghat where Hindu bodies are burned is a cremation ground. A Muslim qabrastaan is a burial ground.",
            "confusion_probe": "Manikarnika Ghat where Hindu bodies are ritually burned is what type of sacred site?",
            "correct_answer": "cremation ground",
            "confused_answer": "burial ground"
        },
        {
            "id": "cul_022",
            "term_a": "sitar",
            "term_b": "sarod",
            "distinction": "Sitar is a long-necked fretted plucked instrument. Sarod is a fretless plucked instrument with deeper bass.",
            "stakes": "medium",
            "correct_context": "The fretted instrument played by Ravi Shankar is sitar. The fretless instrument played by Amjad Ali Khan is sarod.",
            "confusion_probe": "The long-necked fretted instrument most associated with Hindustani classical music played by Ravi Shankar is called what?",
            "correct_answer": "sitar",
            "confused_answer": "sarod"
        },
        {
            "id": "cul_023",
            "term_a": "Kashi",
            "term_b": "Varanasi",
            "distinction": "Kashi is the ancient sacred name meaning City of Light. Varanasi is the modern official name from rivers Varuna and Asi.",
            "stakes": "low",
            "correct_context": "Kashi is used in religious contexts. Varanasi is used in administrative contexts.",
            "confusion_probe": "The ancient Sanskrit name for the holy city on the Ganges meaning City of Light is what?",
            "correct_answer": "Kashi",
            "confused_answer": "Varanasi"
        },
        {
            "id": "cul_024",
            "term_a": "Bodhi tree",
            "term_b": "Ashoka tree",
            "distinction": "The Bodhi tree is the fig tree under which Buddha attained enlightenment. The Ashoka tree is a tree associated with Emperor Ashoka.",
            "stakes": "medium",
            "correct_context": "The fig tree at Bodh Gaya where Buddha sat is the Bodhi tree. The tree planted at Buddhist sites by Ashoka is the Ashoka tree.",
            "confusion_probe": "The sacred fig tree under which Buddha attained enlightenment at Bodh Gaya is called what?",
            "correct_answer": "Bodhi tree",
            "confused_answer": "Ashoka tree"
        },
        {
            "id": "cul_025",
            "term_a": "warp",
            "term_b": "weft",
            "distinction": "Warp is threads stretched lengthwise on the loom. Weft is the thread woven horizontally across the warp.",
            "stakes": "low",
            "correct_context": "The vertical loom threads are warp. The horizontal thread creating the pattern is weft.",
            "confusion_probe": "In Banarasi silk weaving, the horizontal thread passed through vertical loom threads to create brocade patterns is called what?",
            "correct_answer": "weft",
            "confused_answer": "warp"
        },
        {
            "id": "cul_041",
            "term_a": "guru",
            "term_b": "pandit",
            "distinction": "A guru is a spiritual teacher guiding disciples. A pandit is a learned Hindu scholar and priest performing ceremonies.",
            "stakes": "low",
            "correct_context": "A spiritual master initiating disciples into meditation is a guru. A Brahmin officiating at weddings reciting Vedic mantras is a pandit.",
            "confusion_probe": "A learned Hindu scholar and priest who performs Vedic rituals and ceremonies at temples is called what?",
            "correct_answer": "pandit",
            "confused_answer": "guru"
        },
        {
            "id": "cul_042",
            "term_a": "Sanskrit verse",
            "term_b": "Bhojpuri folk song",
            "distinction": "A Sanskrit verse is a formal classical literary composition. A Bhojpuri folk song is an informal oral tradition in the regional language.",
            "stakes": "low",
            "correct_context": "A Ramayana verse in classical Sanskrit meter is a Sanskrit verse. A harvest song in villages around Varanasi is a Bhojpuri folk song.",
            "confusion_probe": "A seasonal harvest song passed down orally through generations in Varanasi villages in the Bhojpuri language is called what?",
            "correct_answer": "Bhojpuri folk song",
            "confused_answer": "Sanskrit verse"
        },
        {
            "id": "cul_043",
            "term_a": "dharamsala",
            "term_b": "temple",
            "distinction": "A dharamsala is a rest house for pilgrims. A temple is a place of worship housing a deity.",
            "stakes": "low",
            "correct_context": "A building near the ghats providing lodging to pilgrims is a dharamsala. The Kashi Vishwanath shrine is a temple.",
            "confusion_probe": "A rest house near the Ganges providing free accommodation to Hindu pilgrims is called what?",
            "correct_answer": "dharamsala",
            "confused_answer": "temple"
        }
    ],
    "emergency_resource": [
        {
            "id": "emr_001",
            "term_a": "blood shortage",
            "term_b": "blood scarcity",
            "distinction": "Blood shortage is a temporary acute deficit at a specific location. Blood scarcity is systemic long-term insufficiency across a region.",
            "stakes": "high",
            "correct_context": "A hospital running out of O-negative after a mass casualty faces shortage. A region chronically unable to meet demand faces scarcity.",
            "confusion_probe": "After a major accident, a hospital exhausts its O-negative supply within hours. What is this acute situation called?",
            "correct_answer": "blood shortage",
            "confused_answer": "blood scarcity"
        },
        {
            "id": "emr_002",
            "term_a": "donor",
            "term_b": "recipient",
            "distinction": "A donor gives blood. A recipient receives blood.",
            "stakes": "high",
            "correct_context": "The person giving blood is the donor. The patient needing transfusion is the recipient.",
            "confusion_probe": "The patient requiring a transfusion during emergency surgery is classified as what?",
            "correct_answer": "recipient",
            "confused_answer": "donor"
        },
        {
            "id": "emr_003",
            "term_a": "priority allocation",
            "term_b": "emergency allocation",
            "distinction": "Priority allocation assigns resources by scoring urgency, compatibility, and distance. Emergency allocation is triggered by critical threshold events overriding normal scoring.",
            "stakes": "high",
            "correct_context": "Routing blood by scoring algorithm is priority allocation. Routing all O-negative to a mass casualty site overriding all other requests is emergency allocation.",
            "confusion_probe": "A scoring algorithm routes blood to patients based on urgency, blood type, and distance. What type of allocation is this?",
            "correct_answer": "priority allocation",
            "confused_answer": "emergency allocation"
        },
        {
            "id": "emr_004",
            "term_a": "triage",
            "term_b": "diagnosis",
            "distinction": "Triage is rapid sorting of patients by urgency. Diagnosis is identification of a specific disease or condition.",
            "stakes": "high",
            "correct_context": "Sorting mass casualty victims by severity is triage. Identifying a ruptured spleen is diagnosis.",
            "confusion_probe": "Medical personnel sort victims into categories by injury severity to determine treatment order. What process is this?",
            "correct_answer": "triage",
            "confused_answer": "diagnosis"
        },
        {
            "id": "emr_005",
            "term_a": "blood type compatibility",
            "term_b": "cross-matching",
            "distinction": "Blood type compatibility is matching ABO and Rh groups. Cross-matching is a lab test mixing donor and recipient blood to check reactions.",
            "stakes": "high",
            "correct_context": "Selecting O-positive blood for an O-positive patient is compatibility. Running a lab test mixing selected donor blood with patient blood is cross-matching.",
            "confusion_probe": "A lab test physically mixing donor and recipient blood to detect incompatibility before transfusion is called what?",
            "correct_answer": "cross-matching",
            "confused_answer": "blood type compatibility"
        },
        {
            "id": "emr_006",
            "term_a": "whole blood",
            "term_b": "packed red blood cells",
            "distinction": "Whole blood contains all components. Packed red blood cells have plasma removed, used for anaemia and blood loss.",
            "stakes": "high",
            "correct_context": "Blood transfused without separation is whole blood. Blood with plasma removed for an anaemic patient is packed red blood cells.",
            "confusion_probe": "A patient with severe anaemia needs red cells with plasma removed to increase oxygen capacity. What product is this?",
            "correct_answer": "packed red blood cells",
            "confused_answer": "whole blood"
        },
        {
            "id": "emr_007",
            "term_a": "universal donor",
            "term_b": "universal recipient",
            "distinction": "Universal donor is O-negative — compatible with any blood type. Universal recipient is AB-positive — can receive any blood type.",
            "stakes": "high",
            "correct_context": "O-negative given to unknown patients is universal donor. AB-positive patients who can receive any type are universal recipients.",
            "confusion_probe": "O-negative blood compatible with all blood types used in emergencies when patient type is unknown is called what?",
            "correct_answer": "universal donor",
            "confused_answer": "universal recipient"
        },
        {
            "id": "emr_008",
            "term_a": "blood bank",
            "term_b": "blood centre",
            "distinction": "A blood bank is hospital-based storing blood for that hospital. A blood centre is standalone collecting and distributing to multiple hospitals.",
            "stakes": "medium",
            "correct_context": "Storage unit within a hospital for surgical patients is a blood bank. Regional facility supplying multiple hospitals is a blood centre.",
            "confusion_probe": "A facility within a hospital storing blood products for that hospital's surgical patients is called what?",
            "correct_answer": "blood bank",
            "confused_answer": "blood centre"
        },
        {
            "id": "emr_009",
            "term_a": "voluntary donation",
            "term_b": "directed donation",
            "distinction": "Voluntary donation is altruistic blood given to general supply. Directed donation is blood given specifically for a named patient.",
            "stakes": "medium",
            "correct_context": "Donating at a blood drive with no specific patient in mind is voluntary. A father donating for his child's surgery is directed.",
            "confusion_probe": "A person donates blood at a community drive with no specific recipient. What type of donation is this?",
            "correct_answer": "voluntary donation",
            "confused_answer": "directed donation"
        },
        {
            "id": "emr_010",
            "term_a": "haemorrhage",
            "term_b": "haematoma",
            "distinction": "Haemorrhage is active bleeding from vessels. Haematoma is a localised collection of blood that has pooled in tissue.",
            "stakes": "high",
            "correct_context": "Blood actively flowing from a ruptured artery is haemorrhage. A pocket of clotted blood under the skull is a haematoma.",
            "confusion_probe": "A patient with a ruptured spleen has blood actively escaping into the abdominal cavity. What is this?",
            "correct_answer": "haemorrhage",
            "confused_answer": "haematoma"
        },
        {
            "id": "emr_011",
            "term_a": "resuscitation",
            "term_b": "stabilisation",
            "distinction": "Resuscitation is emergency restoration of vital functions. Stabilisation is bringing condition under control after resuscitation.",
            "stakes": "high",
            "correct_context": "CPR to restart a stopped heart is resuscitation. Monitoring post-cardiac arrest vitals is stabilisation.",
            "confusion_probe": "A patient receives CPR and defibrillation to restore heartbeat. This restoration of vital functions is called what?",
            "correct_answer": "resuscitation",
            "confused_answer": "stabilisation"
        },
        {
            "id": "emr_012",
            "term_a": "plasma",
            "term_b": "serum",
            "distinction": "Plasma is blood liquid containing clotting factors. Serum is plasma with clotting factors removed after clotting.",
            "stakes": "high",
            "correct_context": "Yellow liquid with fibrinogen is plasma. Liquid remaining after clotting factors are consumed is serum.",
            "confusion_probe": "The liquid component of blood containing clotting factors used in fresh frozen plasma transfusions is called what?",
            "correct_answer": "plasma",
            "confused_answer": "serum"
        },
        {
            "id": "emr_013",
            "term_a": "token reservation",
            "term_b": "direct allocation",
            "distinction": "Token reservation locks a blood unit for a patient in transit preventing reallocation. Direct allocation immediately assigns blood without a lock.",
            "stakes": "high",
            "correct_context": "Locking O-negative for a patient en route is token reservation. Giving the nearest unit to the first requesting patient is direct allocation.",
            "confusion_probe": "A mechanism locking a blood unit for a patient en route to prevent reallocation is called what?",
            "correct_answer": "token reservation",
            "confused_answer": "direct allocation"
        },
        {
            "id": "emr_014",
            "term_a": "spatial clustering",
            "term_b": "priority scoring",
            "distinction": "Spatial clustering groups blood banks by geographic proximity. Priority scoring ranks patients by urgency, compatibility, and distance.",
            "stakes": "medium",
            "correct_context": "Grouping blood banks within 10km using K-means is spatial clustering. Ranking trauma patient above scheduled surgery is priority scoring.",
            "confusion_probe": "Ranking patients by medical urgency, blood type match, and distance to determine who receives scarce units is called what?",
            "correct_answer": "priority scoring",
            "confused_answer": "spatial clustering"
        },
        {
            "id": "emr_015",
            "term_a": "blood group",
            "term_b": "Rh factor",
            "distinction": "Blood group is the ABO classification. Rh factor is the positive or negative antigen classification.",
            "stakes": "high",
            "correct_context": "Whether a patient is A, B, AB, or O is their blood group. Whether positive or negative is their Rh factor.",
            "confusion_probe": "Classification of blood as A, B, AB, or O based on red cell surface antigens is called what?",
            "correct_answer": "blood group",
            "confused_answer": "Rh factor"
        },
        {
            "id": "emr_016",
            "term_a": "expiry",
            "term_b": "contamination",
            "distinction": "Blood expiry is reaching the end of safe storage period. Contamination is infection with pathogens during collection or storage.",
            "stakes": "high",
            "correct_context": "Red cells stored more than 42 days have expired. Red cells infected with bacteria during collection are contaminated.",
            "confusion_probe": "A blood unit stored beyond its 42-day maximum and no longer safe to transfuse has reached what state?",
            "correct_answer": "expiry",
            "confused_answer": "contamination"
        },
        {
            "id": "emr_017",
            "term_a": "mass casualty incident",
            "term_b": "disaster",
            "distinction": "A mass casualty incident produces more patients than local resources can handle. A disaster causes widespread damage not necessarily medical.",
            "stakes": "high",
            "correct_context": "A train derailment overwhelming 3 hospitals is a mass casualty incident. A flood displacing thousands is a disaster.",
            "confusion_probe": "A building collapse produces 150 victims overwhelming nearby hospitals. What emergency term describes this?",
            "correct_answer": "mass casualty incident",
            "confused_answer": "disaster"
        },
        {
            "id": "emr_018",
            "term_a": "haemolytic reaction",
            "term_b": "febrile reaction",
            "distinction": "Haemolytic reaction destroys transfused red cells due to blood type incompatibility. Febrile reaction causes fever and chills without cell destruction.",
            "stakes": "high",
            "correct_context": "Back pain, red urine, and organ failure from incompatible blood is haemolytic. Fever and chills during transfusion without cell destruction is febrile.",
            "confusion_probe": "A patient receiving incompatible blood develops back pain, red urine, and kidney failure. What transfusion reaction is this?",
            "correct_answer": "haemolytic reaction",
            "confused_answer": "febrile reaction"
        },
        {
            "id": "emr_019",
            "term_a": "first responder",
            "term_b": "paramedic",
            "distinction": "A first responder arrives first with basic training. A paramedic is an advanced medical professional with drug administration skills.",
            "stakes": "medium",
            "correct_context": "A police officer with basic CPR arriving first is a first responder. A trained ambulance professional administering drugs is a paramedic.",
            "confusion_probe": "A highly trained medical professional in an ambulance administering medications and performing advanced airway management is called what?",
            "correct_answer": "paramedic",
            "confused_answer": "first responder"
        },
        {
            "id": "emr_020",
            "term_a": "scarcity simulation",
            "term_b": "real inventory data",
            "distinction": "Scarcity simulation artificially reduces blood availability to test allocation under stress. Real inventory data is actual blood unit counts from live records.",
            "stakes": "medium",
            "correct_context": "Artificially setting blood to 20 percent of normal is scarcity simulation. Using actual e-Raktkosh counts is real inventory data.",
            "confusion_probe": "Artificially reducing blood unit availability to 20 percent of normal to test allocation under stress is called what?",
            "correct_answer": "scarcity simulation",
            "confused_answer": "real inventory data"
        }
    ]
}

os.makedirs("data", exist_ok=True)

with open("data/concept_pairs.json", "w", encoding="utf-8") as f:
    json.dump(ALL_PAIRS, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in ALL_PAIRS.values())

print(f"Dataset built from scratch.")
print(f"Medical pairs:           {len(ALL_PAIRS['medical'])}")
print(f"Cultural heritage pairs: {len(ALL_PAIRS['cultural_heritage'])}")
print(f"Emergency resource pairs:{len(ALL_PAIRS['emergency_resource'])}")
print(f"Total pairs:             {total}")
print(f"Status: {'COMPLETE' if total >= 120 else f'NEED {120-total} MORE'}")