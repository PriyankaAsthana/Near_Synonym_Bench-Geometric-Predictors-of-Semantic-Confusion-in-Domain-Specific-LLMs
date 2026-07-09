import json

with open("data/concept_pairs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

FINAL_MEDICAL = [
    {
        "id": "med_041",
        "term_a": "coma",
        "term_b": "vegetative state",
        "distinction": "Coma is a state of complete unconsciousness where the patient cannot be awakened and shows no sleep-wake cycles. Vegetative state is a condition where the patient has sleep-wake cycles and basic reflexes but no awareness or purposeful response.",
        "stakes": "high",
        "correct_context": "A patient with closed eyes, no response to any stimulus, and no sleep-wake cycle is in a coma. A patient who opens eyes spontaneously, has sleep-wake cycles, but shows no awareness is in a vegetative state.",
        "confusion_probe": "A patient opens their eyes spontaneously and has normal sleep-wake cycles but shows absolutely no signs of awareness or purposeful movement. What condition is this?",
        "correct_answer": "vegetative state",
        "confused_answer": "coma"
    },
    {
        "id": "med_042",
        "term_a": "pandemic",
        "term_b": "endemic",
        "distinction": "A pandemic is a disease outbreak spreading globally across multiple countries. An endemic disease is one that is constantly present at a baseline level within a specific geographic region.",
        "stakes": "medium",
        "correct_context": "COVID-19 spreading across every continent in 2020 was a pandemic. Malaria being consistently present in sub-Saharan Africa year after year is endemic.",
        "confusion_probe": "Malaria is consistently present at predictable levels in certain regions of India year after year without spreading globally. What term describes this pattern?",
        "correct_answer": "endemic",
        "confused_answer": "pandemic"
    },
    {
        "id": "med_043",
        "term_a": "intubation",
        "term_b": "ventilation",
        "distinction": "Intubation is the procedure of inserting a tube into the trachea to maintain an airway. Ventilation is the process of mechanically moving air into and out of the lungs — intubation is often performed to enable ventilation.",
        "stakes": "high",
        "correct_context": "A doctor inserting a breathing tube into a patient's throat is performing intubation. The machine then pushing air into the patient's lungs is providing ventilation.",
        "confusion_probe": "The procedure of inserting a tube through a patient's mouth into the trachea to secure the airway is called what?",
        "correct_answer": "intubation",
        "confused_answer": "ventilation"
    }
]

FINAL_CULTURAL = [
    {
        "id": "cul_041",
        "term_a": "guru",
        "term_b": "pandit",
        "distinction": "A guru is a spiritual teacher who guides disciples on a path of spiritual development. A pandit is a learned scholar of Hindu scriptures and rituals — often a priest performing ceremonies.",
        "stakes": "low",
        "correct_context": "A spiritual master who initiates disciples into meditation practice is a guru. A learned Brahmin who officiates at weddings and recites Vedic mantras is a pandit.",
        "confusion_probe": "A learned Hindu scholar and priest who performs Vedic rituals and ceremonies at temples and homes is called what?",
        "correct_answer": "pandit",
        "confused_answer": "guru"
    },
    {
        "id": "cul_042",
        "term_a": "Sanskrit verse",
        "term_b": "Bhojpuri folk song",
        "distinction": "A Sanskrit verse is a formal classical literary composition in the ancient sacred language of Hindu texts. A Bhojpuri folk song is an informal oral tradition in the regional language of eastern Uttar Pradesh and Bihar.",
        "stakes": "low",
        "correct_context": "A verse from the Ramayana composed in classical Sanskrit meter is a Sanskrit verse. A seasonal song sung at harvest time in the villages of Varanasi district in Bhojpuri is a folk song.",
        "confusion_probe": "A seasonal harvest song passed down orally through generations in the villages around Varanasi in the Bhojpuri language is called what?",
        "correct_answer": "Bhojpuri folk song",
        "confused_answer": "Sanskrit verse"
    },
    {
        "id": "cul_043",
        "term_a": "dharamsala",
        "term_b": "temple",
        "distinction": "A dharamsala is a rest house for pilgrims — providing accommodation and basic facilities for travellers on religious journeys. A temple is a place of worship housing a deity.",
        "stakes": "low",
        "correct_context": "A building near the Ganges ghats providing free lodging to pilgrims visiting Varanasi is a dharamsala. The Kashi Vishwanath shrine where Shiva is worshipped is a temple.",
        "confusion_probe": "A rest house near the Ganges ghats providing free accommodation to Hindu pilgrims visiting Varanasi for religious purposes is called what?",
        "correct_answer": "dharamsala",
        "confused_answer": "temple"
    }
]

FINAL_EMERGENCY = [
    {
        "id": "emr_018",
        "term_a": "haemolytic reaction",
        "term_b": "febrile reaction",
        "distinction": "A haemolytic transfusion reaction is a serious immune response where the recipient's immune system destroys the transfused red blood cells due to blood type incompatibility. A febrile reaction is a milder response causing fever and chills during transfusion without cell destruction.",
        "stakes": "high",
        "correct_context": "A patient receiving incompatible blood who develops back pain, haemoglobin in urine, and organ failure is having a haemolytic reaction. A patient developing fever and chills during transfusion with no cell destruction is having a febrile reaction.",
        "confusion_probe": "A patient receiving a blood transfusion develops sudden back pain, red urine, and signs of kidney failure due to blood type incompatibility. What type of transfusion reaction is this?",
        "correct_answer": "haemolytic reaction",
        "confused_answer": "febrile reaction"
    },
    {
        "id": "emr_019",
        "term_a": "first responder",
        "term_b": "paramedic",
        "distinction": "A first responder is any trained individual who arrives first at an emergency scene — police, firefighters, or basic EMTs. A paramedic is a specifically trained advanced medical professional with skills including drug administration and advanced airway management.",
        "stakes": "medium",
        "correct_context": "A police officer trained in basic CPR who arrives first at an accident is a first responder. A trained medical professional in an ambulance who can administer drugs and perform advanced procedures is a paramedic.",
        "confusion_probe": "A highly trained medical professional in an ambulance who can administer medications, perform advanced airway management, and interpret ECGs is called what?",
        "correct_answer": "paramedic",
        "confused_answer": "first responder"
    },
    {
        "id": "emr_020",
        "term_a": "scarcity simulation",
        "term_b": "real inventory data",
        "distinction": "Scarcity simulation artificially reduces available blood units in a model to test allocation behaviour under stress. Real inventory data is actual blood unit counts from live blood bank records.",
        "stakes": "medium",
        "correct_context": "Artificially setting blood availability to 20 percent of normal in a model to test priority allocation is scarcity simulation. Using actual e-Raktkosh blood bank inventory counts in the allocation model is real inventory data.",
        "confusion_probe": "Artificially reducing blood unit availability in a model to 20 percent of normal levels to evaluate how the allocation algorithm performs under stress is called what?",
        "correct_answer": "scarcity simulation",
        "confused_answer": "real inventory data"
    }
]

data["medical"].extend(FINAL_MEDICAL)
data["cultural_heritage"].extend(FINAL_CULTURAL)
data["emergency_resource"].extend(FINAL_EMERGENCY)

with open("data/concept_pairs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = (
    len(data["medical"]) +
    len(data["cultural_heritage"]) +
    len(data["emergency_resource"])
)

print(f"Dataset complete.")
print(f"Medical pairs:           {len(data['medical'])}")
print(f"Cultural heritage pairs: {len(data['cultural_heritage'])}")
print(f"Emergency resource pairs:{len(data['emergency_resource'])}")
print(f"Total pairs:             {total}")
print(f"Target:                  120")
print(f"Status: {'COMPLETE' if total >= 120 else 'INCOMPLETE'}")