import json

with open("data/concept_pairs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

NEW_MEDICAL = [
    {
        "id": "med_026",
        "term_a": "nausea",
        "term_b": "vomiting",
        "distinction": "Nausea is the sensation of needing to vomit without actual expulsion. Vomiting is the forceful expulsion of stomach contents through the mouth.",
        "stakes": "medium",
        "correct_context": "A patient feeling queasy after chemotherapy but not expelling anything has nausea. A patient actively expelling stomach contents is vomiting.",
        "confusion_probe": "A patient feels a strong urge to expel stomach contents but nothing comes out. What is this sensation called?",
        "correct_answer": "nausea",
        "confused_answer": "vomiting"
    },
    {
        "id": "med_027",
        "term_a": "spasticity",
        "term_b": "rigidity",
        "distinction": "Spasticity is velocity-dependent muscle stiffness — resistance increases with speed of movement, seen in stroke and cerebral palsy. Rigidity is constant resistance regardless of movement speed, seen in Parkinson's disease.",
        "stakes": "high",
        "correct_context": "A stroke patient whose arm stiffens more when moved quickly has spasticity. A Parkinson's patient whose arm resists movement equally at all speeds has rigidity.",
        "confusion_probe": "A Parkinson's disease patient has muscle stiffness that resists movement equally regardless of how fast the limb is moved. What is this type of stiffness called?",
        "correct_answer": "rigidity",
        "confused_answer": "spasticity"
    },
    {
        "id": "med_028",
        "term_a": "ischaemia",
        "term_b": "infarction",
        "distinction": "Ischaemia is reduced blood supply to tissue causing temporary dysfunction. Infarction is death of tissue due to complete loss of blood supply.",
        "stakes": "high",
        "correct_context": "Temporary chest pain from reduced coronary blood flow that resolves is ischaemia. Permanent heart muscle death from complete blockage is infarction.",
        "confusion_probe": "A patient has chest pain from reduced blood flow to the heart that resolves completely when they rest. No tissue has died. What is this condition?",
        "correct_answer": "ischaemia",
        "confused_answer": "infarction"
    },
    {
        "id": "med_029",
        "term_a": "dyspnoea",
        "term_b": "apnoea",
        "distinction": "Dyspnoea is difficulty breathing or shortness of breath. Apnoea is complete cessation of breathing.",
        "stakes": "high",
        "correct_context": "A patient struggling to breathe but still breathing has dyspnoea. A patient who has stopped breathing entirely has apnoea.",
        "confusion_probe": "A patient with severe asthma is struggling to breathe but continues to breathe with difficulty. What is this symptom called?",
        "correct_answer": "dyspnoea",
        "confused_answer": "apnoea"
    },
    {
        "id": "med_030",
        "term_a": "ulcer",
        "term_b": "erosion",
        "distinction": "An erosion is a superficial loss of tissue confined to the epithelium. An ulcer is a deeper defect that extends through the epithelium into underlying tissue.",
        "stakes": "medium",
        "correct_context": "A shallow stomach lining defect that does not penetrate the muscle layer is erosion. A deep stomach defect penetrating through the mucosa into muscle is an ulcer.",
        "confusion_probe": "A deep defect in the stomach lining penetrating through the mucosa into the underlying muscle layer is called what?",
        "correct_answer": "ulcer",
        "confused_answer": "erosion"
    },
    {
        "id": "med_031",
        "term_a": "tolerance",
        "term_b": "dependence",
        "distinction": "Tolerance is the reduced effect of a drug over time requiring higher doses for the same effect. Dependence is a physiological or psychological need for a drug to function normally.",
        "stakes": "high",
        "correct_context": "A patient needing higher morphine doses for the same pain relief has developed tolerance. A patient who experiences withdrawal symptoms without morphine has dependence.",
        "confusion_probe": "A pain patient needs progressively higher doses of opioid medication to achieve the same level of pain relief. What has developed?",
        "correct_answer": "tolerance",
        "confused_answer": "dependence"
    },
    {
        "id": "med_032",
        "term_a": "arthritis",
        "term_b": "arthralgia",
        "distinction": "Arthritis is inflammation of a joint with objective signs including swelling, redness, and warmth. Arthralgia is joint pain without objective signs of inflammation.",
        "stakes": "medium",
        "correct_context": "A swollen red hot painful knee with inflammation is arthritis. A painful knee with no swelling or redness is arthralgia.",
        "confusion_probe": "A patient complains of knee pain but examination shows no swelling, redness, or warmth. What is this symptom called?",
        "correct_answer": "arthralgia",
        "confused_answer": "arthritis"
    },
    {
        "id": "med_033",
        "term_a": "contusion",
        "term_b": "laceration",
        "distinction": "A contusion is a bruise — blunt force injury causing bleeding under intact skin. A laceration is a cut or tear through the skin.",
        "stakes": "medium",
        "correct_context": "A black and blue mark under unbroken skin after being hit is a contusion. A cut requiring stitches after a knife injury is a laceration.",
        "confusion_probe": "A patient was hit on the head and has bleeding under intact skin producing a black and blue mark. What type of injury is this?",
        "correct_answer": "contusion",
        "confused_answer": "laceration"
    },
    {
        "id": "med_034",
        "term_a": "hyperthyroidism",
        "term_b": "hypothyroidism",
        "distinction": "Hyperthyroidism is excessive thyroid hormone production causing rapid heart rate, weight loss, and anxiety. Hypothyroidism is insufficient thyroid hormone causing fatigue, weight gain, and depression.",
        "stakes": "high",
        "correct_context": "A patient losing weight with racing heart and feeling hot has hyperthyroidism. A patient gaining weight with fatigue and feeling cold has hypothyroidism.",
        "confusion_probe": "A patient is gaining weight, feels constantly fatigued, is always cold, and has a slow heart rate. What thyroid condition do they have?",
        "correct_answer": "hypothyroidism",
        "confused_answer": "hyperthyroidism"
    },
    {
        "id": "med_035",
        "term_a": "embolism",
        "term_b": "thrombosis",
        "distinction": "Thrombosis is the formation of a blood clot within a vessel at the site of formation. Embolism is the lodging of a travelling clot or other material in a vessel distant from its origin.",
        "stakes": "high",
        "correct_context": "A clot forming in a leg vein is deep vein thrombosis. That clot breaking off and travelling to the lungs is pulmonary embolism.",
        "confusion_probe": "A blood clot that formed in a leg vein breaks off and travels to block a pulmonary artery. What event has occurred in the lung?",
        "correct_answer": "embolism",
        "confused_answer": "thrombosis"
    },
    {
        "id": "med_036",
        "term_a": "cyanosis",
        "term_b": "jaundice",
        "distinction": "Cyanosis is bluish discoloration of skin due to low oxygen in blood. Jaundice is yellow discoloration of skin and eyes due to excess bilirubin.",
        "stakes": "high",
        "correct_context": "Blue lips and fingertips in a patient with low oxygen is cyanosis. Yellow skin and eyes in a patient with liver disease is jaundice.",
        "confusion_probe": "A patient with severe pneumonia develops bluish discoloration of the lips and fingertips due to low blood oxygen. What is this called?",
        "correct_answer": "cyanosis",
        "confused_answer": "jaundice"
    },
    {
        "id": "med_037",
        "term_a": "tinnitus",
        "term_b": "vertigo",
        "distinction": "Tinnitus is a ringing or buzzing sound in the ears without external source. Vertigo is a sensation of spinning or movement when stationary.",
        "stakes": "medium",
        "correct_context": "A patient hearing constant ringing with no external source has tinnitus. A patient feeling the room is spinning when lying still has vertigo.",
        "confusion_probe": "A patient experiences a persistent ringing sound in both ears with no external source present. What is this condition called?",
        "correct_answer": "tinnitus",
        "confused_answer": "vertigo"
    }
]

NEW_CULTURAL = [
    {
        "id": "cul_026",
        "term_a": "bhajan",
        "term_b": "kirtan",
        "distinction": "A bhajan is a devotional song sung individually or in a group for personal spiritual practice. A kirtan is a call-and-response devotional chanting practice in a congregational setting.",
        "stakes": "low",
        "correct_context": "A devotional song sung individually during morning prayer is a bhajan. A call-and-response chanting session in a temple with a leader and congregation is kirtan.",
        "confusion_probe": "A congregational call-and-response devotional chanting session in a Varanasi temple where a leader sings and devotees respond is called what?",
        "correct_answer": "kirtan",
        "confused_answer": "bhajan"
    },
    {
        "id": "cul_027",
        "term_a": "karma yoga",
        "term_b": "jnana yoga",
        "distinction": "Karma yoga is the path of selfless action — performing duties without attachment to results. Jnana yoga is the path of knowledge and wisdom — liberation through intellectual understanding of reality.",
        "stakes": "medium",
        "correct_context": "A person serving others without expectation of reward follows karma yoga. A person studying Vedantic philosophy to understand the nature of Brahman follows jnana yoga.",
        "confusion_probe": "The spiritual path of performing one's duties selflessly without attachment to results described in the Bhagavad Gita is called what?",
        "correct_answer": "karma yoga",
        "confused_answer": "jnana yoga"
    },
    {
        "id": "cul_028",
        "term_a": "Shiva",
        "term_b": "Vishnu",
        "distinction": "Shiva is the Hindu deity of destruction and transformation, worshipped as the supreme being in Shaivism. Vishnu is the Hindu deity of preservation and protection, worshipped as the supreme being in Vaishnavism.",
        "stakes": "medium",
        "correct_context": "The deity worshipped at Kashi Vishwanath temple in Varanasi is Shiva. The deity whose avatars include Rama and Krishna is Vishnu.",
        "confusion_probe": "The Hindu deity of destruction and transformation worshipped as the supreme being at Kashi Vishwanath temple in Varanasi is called what?",
        "correct_answer": "Shiva",
        "confused_answer": "Vishnu"
    },
    {
        "id": "cul_029",
        "term_a": "Diwali",
        "term_b": "Holi",
        "distinction": "Diwali is the Hindu festival of lights celebrating the return of Rama, marked by lamps and fireworks. Holi is the Hindu festival of colours celebrating the arrival of spring and the victory of good over evil.",
        "stakes": "low",
        "correct_context": "The festival where families light diyas and burst fireworks in October or November is Diwali. The festival where people throw coloured powder and water in March is Holi.",
        "confusion_probe": "The Hindu festival celebrated by lighting oil lamps and bursting fireworks to mark the return of Lord Rama is called what?",
        "correct_answer": "Diwali",
        "confused_answer": "Holi"
    },
    {
        "id": "cul_030",
        "term_a": "sutradhar",
        "term_b": "narrator",
        "distinction": "A sutradhar is the traditional director and stage manager in Indian classical theatre who also participates as a character. A narrator is a modern storytelling voice that describes events from outside the story.",
        "stakes": "low",
        "correct_context": "The character in Sanskrit drama who introduces the play, manages the stage, and interacts with other characters is the sutradhar. A voice describing events in a modern novel from outside is a narrator.",
        "confusion_probe": "In traditional Sanskrit theatre, the character who introduces the play, manages the stage, and interacts with other characters is called what?",
        "correct_answer": "sutradhar",
        "confused_answer": "narrator"
    },
    {
        "id": "cul_031",
        "term_a": "vipassana",
        "term_b": "samatha",
        "distinction": "Vipassana is insight meditation focused on observing the impermanence of experience. Samatha is calm-abiding meditation focused on concentrating the mind on a single object to develop tranquillity.",
        "stakes": "medium",
        "correct_context": "Meditating by observing the arising and passing of sensations without reaction is vipassana. Meditating by focusing on the breath to develop a calm concentrated mind is samatha.",
        "confusion_probe": "The Buddhist meditation practice of observing the impermanence of bodily sensations and mental events without reaction is called what?",
        "correct_answer": "vipassana",
        "confused_answer": "samatha"
    },
    {
        "id": "cul_032",
        "term_a": "Mahabharata",
        "term_b": "Bhagavad Gita",
        "distinction": "The Mahabharata is the ancient Sanskrit epic narrating the Kurukshetra war between the Pandavas and Kauravas. The Bhagavad Gita is a section within the Mahabharata — a philosophical dialogue between Krishna and Arjuna.",
        "stakes": "medium",
        "correct_context": "The full epic poem narrating the war between cousins is the Mahabharata. The 18-chapter dialogue on duty and liberation within that epic is the Bhagavad Gita.",
        "confusion_probe": "The 700-verse philosophical dialogue between Krishna and the warrior Arjuna that forms part of a larger Sanskrit epic is called what?",
        "correct_answer": "Bhagavad Gita",
        "confused_answer": "Mahabharata"
    },
    {
        "id": "cul_033",
        "term_a": "namaskar",
        "term_b": "pranaam",
        "distinction": "Namaskar is a respectful greeting with palms joined meaning I bow to the divine in you. Pranaam is a deeper gesture of reverence — bowing or touching feet of elders or deities.",
        "stakes": "low",
        "correct_context": "Joining palms and saying namaskar when meeting someone is namaskar. Touching the feet of grandparents to seek their blessings is pranaam.",
        "confusion_probe": "The act of touching the feet of an elder or deity in deep reverence to seek blessings is called what in Indian tradition?",
        "correct_answer": "pranaam",
        "confused_answer": "namaskar"
    },
    {
        "id": "cul_034",
        "term_a": "tilak",
        "term_b": "bindi",
        "distinction": "A tilak is a mark applied on the forehead during religious rituals indicating spiritual significance or sectarian identity. A bindi is a decorative dot worn by women on the forehead as a cultural or aesthetic marker.",
        "stakes": "low",
        "correct_context": "The sandalwood or ash mark applied by a priest on a worshipper's forehead during puja is a tilak. The red dot worn by a married Hindu woman daily is a bindi.",
        "confusion_probe": "The mark applied on the forehead by a priest during a Hindu religious ceremony indicating spiritual significance is called what?",
        "correct_answer": "tilak",
        "confused_answer": "bindi"
    },
    {
        "id": "cul_035",
        "term_a": "Theravada",
        "term_b": "Mahayana",
        "distinction": "Theravada is the oldest surviving school of Buddhism emphasising individual liberation through the Eightfold Path. Mahayana is a later school emphasising the bodhisattva ideal — achieving enlightenment for the benefit of all beings.",
        "stakes": "medium",
        "correct_context": "The Buddhism practised in Sri Lanka and Thailand following the Pali Canon is Theravada. The Buddhism of Tibet, China, and Japan emphasising the bodhisattva path is Mahayana.",
        "confusion_probe": "The oldest surviving school of Buddhism practised in Sri Lanka and Southeast Asia that focuses on individual liberation through the Eightfold Path is called what?",
        "correct_answer": "Theravada",
        "confused_answer": "Mahayana"
    },
    {
        "id": "cul_036",
        "term_a": "dhrupad",
        "term_b": "khayal",
        "distinction": "Dhrupad is the oldest surviving form of Hindustani classical vocal music — austere, meditative, using Sanskrit texts. Khayal is the more popular later form — flexible, ornate, using Urdu and Hindi texts.",
        "stakes": "medium",
        "correct_context": "The ancient austere Sanskrit-based vocal form performed at the Kashi Vishwanath temple is dhrupad. The flexible ornate vocal form with Urdu compositions performed in concerts is khayal.",
        "confusion_probe": "The oldest surviving form of Hindustani vocal music that is austere, meditative, and uses Sanskrit texts is called what?",
        "correct_answer": "dhrupad",
        "confused_answer": "khayal"
    },
    {
        "id": "cul_037",
        "term_a": "Ganges",
        "term_b": "Yamuna",
        "distinction": "The Ganges is the most sacred river in Hinduism flowing through Varanasi. The Yamuna is the second most sacred Hindu river flowing through Mathura and Vrindavan associated with Krishna.",
        "stakes": "medium",
        "correct_context": "The river at whose banks the ghats of Varanasi are built is the Ganges. The river associated with Krishna's childhood in Mathura is the Yamuna.",
        "confusion_probe": "The most sacred river in Hinduism that flows through Varanasi at whose banks pilgrims perform ritual bathing is called what?",
        "correct_answer": "Ganges",
        "confused_answer": "Yamuna"
    }
]

NEW_EMERGENCY = [
    {
        "id": "emr_021",
        "term_a": "autologous transfusion",
        "term_b": "allogeneic transfusion",
        "distinction": "Autologous transfusion is transfusing a patient with their own previously donated blood. Allogeneic transfusion is transfusing blood donated by another person.",
        "stakes": "high",
        "correct_context": "A patient donating their own blood before planned surgery to be given back during the operation is autologous. A patient receiving blood from a blood bank donor is allogeneic.",
        "confusion_probe": "A surgical patient receives blood they donated themselves before the operation. What type of transfusion is this?",
        "correct_answer": "autologous transfusion",
        "confused_answer": "allogeneic transfusion"
    },
    {
        "id": "emr_022",
        "term_a": "hypothermia",
        "term_b": "hyperthermia",
        "distinction": "Hypothermia is dangerously low body temperature below 35 degrees Celsius. Hyperthermia is dangerously high body temperature above 40 degrees Celsius.",
        "stakes": "high",
        "correct_context": "A patient rescued from cold water with body temperature of 32 degrees has hypothermia. A patient with heat stroke at 41 degrees has hyperthermia.",
        "confusion_probe": "A patient rescued from cold water has a core body temperature of 32 degrees Celsius. What condition is this?",
        "correct_answer": "hypothermia",
        "confused_answer": "hyperthermia"
    },
    {
        "id": "emr_023",
        "term_a": "haemostasis",
        "term_b": "anticoagulation",
        "distinction": "Haemostasis is the process of stopping bleeding through clot formation. Anticoagulation is the use of drugs to prevent or dissolve blood clots.",
        "stakes": "high",
        "correct_context": "The body forming a clot to stop bleeding from a cut is haemostasis. Giving heparin to prevent clots in a bedridden patient is anticoagulation.",
        "confusion_probe": "The physiological process by which the body stops bleeding through platelet aggregation and clot formation is called what?",
        "correct_answer": "haemostasis",
        "confused_answer": "anticoagulation"
    },
    {
        "id": "emr_024",
        "term_a": "cardiac output",
        "term_b": "blood pressure",
        "distinction": "Cardiac output is the volume of blood the heart pumps per minute. Blood pressure is the force exerted by circulating blood on vessel walls.",
        "stakes": "high",
        "correct_context": "A heart pumping 5 litres of blood per minute has a cardiac output of 5L per minute. The 120/80 mmHg reading on a sphygmomanometer is blood pressure.",
        "confusion_probe": "The total volume of blood pumped by the heart in one minute is called what?",
        "correct_answer": "cardiac output",
        "confused_answer": "blood pressure"
    },
    {
        "id": "emr_025",
        "term_a": "platelet transfusion",
        "term_b": "red cell transfusion",
        "distinction": "Platelet transfusion provides clotting cells for patients with low platelet counts causing bleeding risk. Red cell transfusion provides oxygen-carrying cells for anaemic patients.",
        "stakes": "high",
        "correct_context": "A chemotherapy patient with dangerously low platelets at risk of bleeding receives platelet transfusion. An anaemic patient with haemoglobin of 6 receives red cell transfusion.",
        "confusion_probe": "A patient with severe anaemia and haemoglobin of 6 needs transfusion to improve oxygen delivery to tissues. What type of transfusion is this?",
        "correct_answer": "red cell transfusion",
        "confused_answer": "platelet transfusion"
    },
    {
        "id": "emr_026",
        "term_a": "acute blood loss",
        "term_b": "chronic blood loss",
        "distinction": "Acute blood loss is sudden rapid loss of large blood volume from trauma or haemorrhage. Chronic blood loss is slow ongoing loss over time causing gradual anaemia.",
        "stakes": "high",
        "correct_context": "Bleeding rapidly from a stab wound losing 2 litres in 10 minutes is acute blood loss. Slowly bleeding from a gastric ulcer over months causing gradual anaemia is chronic blood loss.",
        "confusion_probe": "A patient has been slowly losing blood from a gastric ulcer for 6 months developing gradual anaemia. What type of blood loss is this?",
        "correct_answer": "chronic blood loss",
        "confused_answer": "acute blood loss"
    },
    {
        "id": "emr_027",
        "term_a": "informed consent",
        "term_b": "implied consent",
        "distinction": "Informed consent is explicit agreement from a conscious patient after being given information about risks and benefits. Implied consent is assumed consent in emergencies when the patient is unconscious.",
        "stakes": "high",
        "correct_context": "A conscious patient signing a form agreeing to surgery after explanation is informed consent. Treating an unconscious accident victim without explicit agreement assuming they would consent is implied consent.",
        "confusion_probe": "An unconscious accident victim is treated by paramedics assuming they would consent to life-saving intervention. What type of consent is this?",
        "correct_answer": "implied consent",
        "confused_answer": "informed consent"
    },
    {
        "id": "emr_028",
        "term_a": "field triage",
        "term_b": "hospital triage",
        "distinction": "Field triage is rapid patient sorting at the emergency scene before transport. Hospital triage is systematic patient sorting at the emergency department on arrival.",
        "stakes": "high",
        "correct_context": "A paramedic tagging accident victims at the crash site by severity is field triage. A nurse assessing patients as they arrive at the emergency department is hospital triage.",
        "confusion_probe": "A paramedic at a road accident scene rapidly categorises victims by injury severity before deciding transport priority. What is this process called?",
        "correct_answer": "field triage",
        "confused_answer": "hospital triage"
    },
    {
        "id": "emr_029",
        "term_a": "defibrillation",
        "term_b": "cardioversion",
        "distinction": "Defibrillation delivers an unsynchronised high-energy shock to stop ventricular fibrillation. Cardioversion delivers a synchronised lower-energy shock timed to the QRS complex to restore normal rhythm.",
        "stakes": "high",
        "correct_context": "Shocking a patient in ventricular fibrillation with maximum energy is defibrillation. Delivering a timed shock to convert atrial fibrillation is cardioversion.",
        "confusion_probe": "A patient in ventricular fibrillation with no organised cardiac rhythm receives an unsynchronised high-energy electric shock. What procedure is this?",
        "correct_answer": "defibrillation",
        "confused_answer": "cardioversion"
    },
    {
        "id": "emr_030",
        "term_a": "blood volume",
        "term_b": "blood count",
        "distinction": "Blood volume is the total amount of blood in the body measured in litres. Blood count is a laboratory test measuring the number of different blood cell types per unit volume.",
        "stakes": "medium",
        "correct_context": "An adult human having approximately 5 litres of blood in their body is blood volume. A CBC showing red cells, white cells, and platelet numbers is a blood count.",
        "confusion_probe": "A laboratory test measuring the number of red blood cells, white blood cells, and platelets per microlitre of blood is called what?",
        "correct_answer": "blood count",
        "confused_answer": "blood volume"
    },
    {
        "id": "emr_031",
        "term_a": "shock",
        "term_b": "collapse",
        "distinction": "Shock is a life-threatening medical condition of inadequate tissue perfusion causing organ failure. Collapse is a non-specific term for sudden loss of ability to stand or remain conscious.",
        "stakes": "high",
        "correct_context": "A patient with low blood pressure, rapid heart rate, and organ failure from blood loss is in shock. A patient who suddenly falls to the ground unconscious has collapsed.",
        "confusion_probe": "A patient with severe blood loss develops dangerously low blood pressure, rapid heart rate, and signs of organ failure. What medical condition is this?",
        "correct_answer": "shock",
        "confused_answer": "collapse"
    },
    {
        "id": "emr_032",
        "term_a": "oxygen saturation",
        "term_b": "oxygen partial pressure",
        "distinction": "Oxygen saturation is the percentage of haemoglobin carrying oxygen measured by pulse oximeter. Oxygen partial pressure is the pressure exerted by oxygen in blood measured by arterial blood gas.",
        "stakes": "high",
        "correct_context": "The 98% reading on a pulse oximeter clipped to a finger is oxygen saturation. The pO2 value on an arterial blood gas report is oxygen partial pressure.",
        "confusion_probe": "The percentage of haemoglobin molecules that are carrying oxygen measured non-invasively by a finger clip device is called what?",
        "correct_answer": "oxygen saturation",
        "confused_answer": "oxygen partial pressure"
    },
    {
        "id": "emr_033",
        "term_a": "blood bank inventory",
        "term_b": "blood bank demand",
        "distinction": "Blood bank inventory is the actual stock of available blood units. Blood bank demand is the forecasted or actual need for blood units from clinical requests.",
        "stakes": "high",
        "correct_context": "A blood bank holding 200 units of O-positive has an inventory of 200. Hospitals requesting 350 units represents demand exceeding inventory.",
        "confusion_probe": "The actual number of blood units physically present and available in a blood bank at a given time is called what?",
        "correct_answer": "blood bank inventory",
        "confused_answer": "blood bank demand"
    },
    {
        "id": "emr_034",
        "term_a": "cold chain",
        "term_b": "warm chain",
        "distinction": "Cold chain is the temperature-controlled supply chain maintaining blood products at required refrigeration temperatures during storage and transport. Warm chain refers to maintaining warm temperatures for patients during emergency care.",
        "stakes": "high",
        "correct_context": "Keeping red blood cells between 2-6 degrees Celsius from donation to transfusion is the cold chain. Keeping a hypothermic patient warm during transport is the warm chain.",
        "confusion_probe": "The system that maintains red blood cells at 2-6 degrees Celsius from donation through storage and transport to transfusion is called what?",
        "correct_answer": "cold chain",
        "confused_answer": "warm chain"
    },
    {
        "id": "emr_035",
        "term_a": "haemovigilance",
        "term_b": "pharmacovigilance",
        "distinction": "Haemovigilance is the surveillance system for monitoring adverse events related to blood transfusion. Pharmacovigilance is the surveillance system for monitoring adverse effects of drugs and medicines.",
        "stakes": "medium",
        "correct_context": "A national system tracking transfusion reactions and errors is haemovigilance. A national system tracking adverse drug reactions is pharmacovigilance.",
        "confusion_probe": "A national surveillance system that monitors and records adverse reactions and errors related to blood transfusion is called what?",
        "correct_answer": "haemovigilance",
        "confused_answer": "pharmacovigilance"
    },
    {
        "id": "emr_036",
        "term_a": "transfusion trigger",
        "term_b": "transfusion threshold",
        "distinction": "Transfusion trigger is the clinical decision point at which a specific patient's condition warrants transfusion based on their individual circumstances. Transfusion threshold is the standardised haemoglobin level below which transfusion is generally recommended by guidelines.",
        "stakes": "high",
        "correct_context": "A haemoglobin level of 7g/dL below which guidelines recommend transfusion is the threshold. A clinician deciding this specific patient with heart disease needs transfusion at 9g/dL based on symptoms is the trigger.",
        "confusion_probe": "The standardised haemoglobin level recommended in clinical guidelines below which blood transfusion should generally be considered is called what?",
        "correct_answer": "transfusion threshold",
        "confused_answer": "transfusion trigger"
    },
    {
        "id": "emr_037",
        "term_a": "blood wastage",
        "term_b": "blood shortage",
        "distinction": "Blood wastage is discarding usable blood due to expiry, mishandling, or over-ordering. Blood shortage is insufficient blood supply to meet clinical demand.",
        "stakes": "high",
        "correct_context": "A hospital discarding expired unused blood units is wastage. A hospital unable to fulfil transfusion requests because stocks are depleted is shortage.",
        "confusion_probe": "A hospital discards 50 units of red blood cells because they expired before being used. What problem does this represent?",
        "correct_answer": "blood wastage",
        "confused_answer": "blood shortage"
    },
    {
        "id": "emr_038",
        "term_a": "point of care testing",
        "term_b": "laboratory testing",
        "distinction": "Point of care testing performs diagnostic tests at or near the patient bedside giving rapid results. Laboratory testing processes samples in a central laboratory with higher accuracy but longer turnaround time.",
        "stakes": "medium",
        "correct_context": "A bedside blood glucose meter giving results in 10 seconds is point of care testing. Sending a blood sample to the hospital laboratory for full blood count is laboratory testing.",
        "confusion_probe": "A blood glucose test performed at the patient's bedside using a handheld device giving results within seconds is called what type of testing?",
        "correct_answer": "point of care testing",
        "confused_answer": "laboratory testing"
    },
    {
        "id": "emr_039",
        "term_a": "massive transfusion",
        "term_b": "routine transfusion",
        "distinction": "Massive transfusion is the replacement of more than one blood volume within 24 hours or more than 10 units in a few hours typically in trauma. Routine transfusion is elective transfusion of 1-2 units for chronic anaemia management.",
        "stakes": "high",
        "correct_context": "A trauma patient receiving 15 units of red cells in 6 hours is massive transfusion. An anaemic dialysis patient receiving 2 units every month is routine transfusion.",
        "confusion_probe": "A trauma patient requires more than 10 units of blood within a few hours to replace catastrophic blood loss. What type of transfusion is this?",
        "correct_answer": "massive transfusion",
        "confused_answer": "routine transfusion"
    },
    {
        "id": "emr_040",
        "term_a": "donor deferral",
        "term_b": "donor rejection",
        "distinction": "Donor deferral is temporary postponement of blood donation due to a reversible condition such as recent illness or travel. Donor rejection is permanent exclusion from donation due to an irresolvable risk factor.",
        "stakes": "medium",
        "correct_context": "Telling a donor to wait 6 months after visiting a malaria zone before donating is deferral. Permanently excluding a donor with HIV from ever donating is rejection.",
        "confusion_probe": "A blood donor is told to wait 6 months before donating because they recently returned from a malaria-endemic country. What is this called?",
        "correct_answer": "donor deferral",
        "confused_answer": "donor rejection"
    }
]

data["medical"].extend(NEW_MEDICAL)
data["cultural_heritage"].extend(NEW_CULTURAL)
data["emergency_resource"].extend(NEW_EMERGENCY)

with open("data/concept_pairs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = sum(len(v) for v in data.values())

print(f"Dataset complete.")
print(f"Medical pairs:           {len(data['medical'])}")
print(f"Cultural heritage pairs: {len(data['cultural_heritage'])}")
print(f"Emergency resource pairs:{len(data['emergency_resource'])}")
print(f"Total pairs:             {total}")
print(f"Status: {'COMPLETE' if total >= 120 else f'NEED {120-total} MORE'}")