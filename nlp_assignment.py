
import spacy
import re
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

nlp = spacy.load("en_core_web_lg")

TASK_VERBS = {
    "complete", "prepare", "submit", "deliver", "schedule", "finalize", "review",
    "organize", "arrange", "plan", "draft", "finish", "execute", "update", "write", "solve",
    "approve", "delegate", "coordinate", "call", "remind", "book", "design", "develop", "pick",
    "cook", "report", "document", "summarize", "record", "log", "note down", "jot down",
    "keep track of", "file", "scribble", "write up", "noting", "paperwork", "register",
    "make an entry", "fill form", "apply", "meeting", "appointment", "conference", "set up",
    "plan a meet-up", "book a slot", "catch up", "sync up", "fix a time", "block time", "set reminder",
    "pickup", "transport", "ship", "dispatch", "procure", "supply", "collect", "drop off", "grab",
    "run an errand", "send out", "bring over", "courier", "parcel", "code", "program", "build",
    "prototype", "launch", "debug", "patch", "deploy", "write code", "fix a bug", "test a feature",
    "server restart kar", "deploy karna hai", "api hit kar", "feature add kar", "research", "analyze",
    "study", "investigate", "examine", "assess", "look into", "fact-check", "find out", "double-check",
    "support", "assist", "help", "resolve", "troubleshoot", "fix", "address", "sort out", "guide",
    "take care of", "check on", "follow up", "lend a hand", "market", "sell", "advertise", "promote",
    "campaign", "outreach", "prospect", "pitch", "spread the word", "recommend", "post about", "boost",
    "shout out", "recruit", "interview", "onboard", "hire", "evaluate", "appraise",
    "hr", "team up", "budget", "finance", "invoice", "expense", "cost", "profit", "account", "audit",
    "reimbursement", "administer", "manage", "supervise", "oversee", "monitor", "operate", "comply",
    "legal", "policy", "regulation", "contract", "implement", "rti file karna", "adhar link karna",
    "rule follow karna", "court ka kaam", "network", "install", "upgrade", "configure", "maintain",
    "secure", "internet setup karna", "router reset karna", "watch", "movie", "play", "game", "listen",
    "music", "read", "book", "watching", "exercise", "work out", "run", "jog", "gym", "walk", "meditate",
    "yoga", "morning walk", "project", "milestone", "deliverable", "track", "progress", "text", "message",
    "visit", "check in", "hang out", "buy snacks", "buy food", "clean", "wash", "laundry", "vacuum", "mop",
    "dust", "dinner duty", "make dinner", "bartan dhona", "kapde dhona", "jhadoo lagana", "gas bhara hai?",
    "roti banana", "innovate", "experiment", "communicate", "announce", "press", "media", "public",
    "broadcast", "engage", "event", "host", "repair", "service", "upkeep", "restore", "purchase",
    "inventory", "order", "stock", "vendor", "negotiate"
}

TIME_KEYWORDS = {
    "morning", "afternoon", "evening", "night", "today", "tomorrow", "yesterday",
    "noon", "midnight", "hour", "minute", "second", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday", "deadline", "due date", "asap",
    "later", "in a bit", "end of the day", "right away", "soon", "eventually", "afterwards",
    "next week", "next month", "in the future", "by", "until", "from", "to", "between", "during",
    "weekly", "monthly", "annually", "daily", "hourly"
}

# TIME_KEYWORDS = {kw.lower() for kw in TIME_KEYWORDS}

CATEGORIES = {
    "Documentation & Reporting": {"report", "draft", "document", "write", "summarize", "record", "log", "note", "paperwork", "register", "file"},
    "Meetings & Scheduling": {"meeting", "schedule", "arrange", "appointment", "conference", "call", "setup", "plan", "book", "sync", "reminder"},
    "Logistics & Delivery": {"deliver", "pickup", "transport", "ship", "dispatch", "procure", "supply", "collect", "drop", "grab", "errand", "courier", "parcel"},
    "Software Development": {"develop", "design", "code", "program", "build", "prototype", "launch", "debug", "deploy", "test", "feature", "integrate"},
    "Research & Analysis": {"research", "analyze", "review", "study", "investigate", "examine", "assess", "fact-check", "evaluate"},
    "Customer Support": {"support", "assist", "help", "resolve", "troubleshoot", "address", "guide", "follow"},
    "Sales & Marketing": {"market", "sell", "advertise", "promote", "campaign", "outreach", "prospect", "pitch"},
    "Human Resources": {"recruit", "interview", "onboard", "hire", "evaluate", "appraise", "human resources", "hiring", "onboarding", "recruitment"},
    "Finance & Accounting": {"budget", "finance", "invoice", "expense", "cost", "profit", "account", "audit", "accounting", "financial", "tax"},
    "Operations & Administration": {"administer", "manage", "coordinate", "supervise", "oversee", "monitor", "operate", "operations", "administration", "handle", "organize"},
    "Legal & Compliance": {"comply", "legal", "policy", "regulation", "contract", "implement", "court", "compliance", "legalities"},
    "IT & Infrastructure": {"network", "install", "upgrade", "configure", "maintain", "secure", "monitor", "infrastructure", "server", "database", "system", "technical", "technology"},
    "Project Management": {"project", "plan", "milestone", "deliverable", "track", "update", "progress", "management", "task"},
    "Training & Development": {"train", "workshop", "seminar", "educate", "coach", "instruct", "learn", "development", "upskill"},
    "Quality Assurance": {"test", "quality", "validate", "inspect", "assess", "double-check", "quality assurance", "testing"},
    "Procurement & Inventory": {"procure", "purchase", "inventory", "order", "stock", "vendor", "negotiate", "procurement", "inventory management"},
    "Maintenance & Repairs": {"maintain", "repair", "fix", "service", "upkeep", "restore", "troubleshoot", "maintenance", "repairs"},
    "Event Planning": {"event", "organize", "host", "coordinate", "arrange", "event planning", "management", "planning"},
    "Public Relations & Communication": {"communicate", "announce", "press", "media", "broadcast", "engage", "public relations", "communication"},
    "Innovation & R&D": {"innovate", "experiment", "prototype", "develop", "research", "innovation", "r&d", "experimentation"},
    "Household Chores": {"clean", "cook", "wash", "laundry", "vacuum", "mop", "dust", "housekeeping", "cleaning", "cooking"},
    "Social & Personal Tasks": {"call", "text", "message", "visit", "hang out", "social", "personal", "errand", "buy snacks"},
    "Health & Fitness": {"exercise", "workout", "run", "jog", "gym", "walk", "meditate", "yoga", "fitness", "physical"},
    "Leisure & Entertainment": {"watch", "movie", "play", "game", "listen", "music", "read", "book", "netflix", "entertainment", "hobby", "recreation"}
}

OBLIGATION_PHRASES = ["has to", "have to", "needs to", "must", "should", "ought to", "need to", "required to", "make sure to", "ensure to", "important to", "crucial to", "essential to", "necessary to", "imperative to", "vital to"]
MODAL_VERBS = ["will", "would", "can", "could", "may", "might", "shall", "should", "must", "need", "ought to"]
QUESTION_WORDS = ["how", "what", "when", "where", "why", "who", "whom", "which", "is", "are", "am", "do", "does", "did", "has", "have", "had", "can", "could", "will", "would", "may", "might", "shall", "should", "must", "need", "ought to", "whether", "if"]
NON_TASK_KEYWORDS = {"nothing", "anything", "everything", "something", "awkward", "kidding", "joke", "about", "this", "that", "just", "only", "actually", "mean", "meanwhile", "anyway", "however", "yet", "still", "though", "although", "but", "and", "or", "because", "since", "when", "while", "if", "unless", "until", "rather", "instead", "nevertheless", "nonetheless", "conversely", "likewise", "similarly", "furthermore", "moreover", "in addition", "also", "besides", "too", "as well", "then", "so", "therefore", "thus", "consequently", "hence", "accordingly", "thereby", "whereby", "therein", "whereupon", "wherefore", "whenever", "wherever", "whoever", "whomever", "whichever", "whatever", "who", "what", "when", "where", "why", "how", "which", "whom", "everyone", "everything", "anyone", "anybody", "nobody", "someone", "somebody", "thing", "things", "doing", "do", "does", "did", "done", "today", "yesterday", "tomorrow", "day"}

CASUAL_INDICATORS = ["just kidding", "i mean", "ha", "haha", "joke"]


def contains_obligation_phrase(text_lower):
    return any(phrase in text_lower for phrase in OBLIGATION_PHRASES)

def has_task_verb_direct(doc):
    for token in doc:
        if token.head == token and token.pos_ == "VERB" and token.lemma_.lower() in TASK_VERBS:
            return True
    return False

def has_task_verb_synonyms(doc):
    for token in doc:
        if token.pos_ == "VERB":
            lemma = token.lemma_.lower()
            if lemma in TASK_VERBS:
                return True
            synsets = wn.synsets(lemma, pos=wn.VERB)
            if synsets:
                related_lemmas = set()
                for syn in synsets:
                    related_lemmas.update(l.lower() for l in syn.lemma_names())
                    for hyper in syn.hypernyms():
                        related_lemmas.update(l.lower() for l in hyper.lemma_names())
                if any(rel in TASK_VERBS for rel in related_lemmas):
                    return True
    return False

def detect_modal_task(doc):
    for token in doc:
        if token.text.lower() in MODAL_VERBS and token.dep_ in ("aux", "auxpass"):
            head_verb = token.head
            if head_verb.pos_ == "VERB" and head_verb.lemma_.lower() in TASK_VERBS:
                return True
            synsets = wn.synsets(head_verb.lemma_.lower(), pos=wn.VERB)
            if synsets:
                related_lemmas = set()
                for syn in synsets:
                    related_lemmas.update(l.lower() for l in syn.lemma_names())
                    for hyper in syn.hypernyms():
                        related_lemmas.update(l.lower() for l in hyper.lemma_names())
                if any(rel in TASK_VERBS for rel in related_lemmas):
                    return True
    return False

def detect_imperative_task(doc):
    if not doc or doc[0].pos_ != "VERB":
        return False
    if doc[0].tag_ == "VB":
        if len(doc) > 1 and doc[1].pos_ in ["ADV", "INTJ", "PART"] and doc[1].dep_ == "advmod":
            return False
        if not any(child.dep_ in ("dobj", "iobj", "pobj", "attr") for child in doc[0].children):
            return False
        return True
    if doc[0].lemma_.lower() in TASK_VERBS:
        if len(doc) > 1 and doc[1].pos_ in ["ADV", "INTJ", "PART"] and doc[1].dep_ == "advmod":
            return False
        if not any(child.dep_ in ("dobj", "iobj", "pobj", "attr") for child in doc[0].children):
            return False
        return True
    return False

def is_task_sentence(sentence):
    text_lower = sentence.lower()
    if contains_obligation_phrase(text_lower):
        return True
    if sentence.lower().startswith(tuple(QUESTION_WORDS)) or sentence.endswith("?"):
        return False
    doc = nlp(sentence)
    non_task_count = sum(1 for token in doc if token.lemma_.lower() in NON_TASK_KEYWORDS and not token.is_punct)
    total_words = sum(1 for token in doc if not token.is_punct)
    if total_words > 0 and (non_task_count / total_words) >= 0.6:
        return False
    has_person = any(ent.label_ == "PERSON" for ent in doc.ents)
    if has_person and (has_task_verb_direct(doc) or has_task_verb_synonyms(doc)):
        return True
    if detect_modal_task(doc) or detect_imperative_task(doc):
        return True
    return False

def split_into_clauses(sentence):
    clauses = re.split(r',|;| and ', sentence)
    cleaned = []
    for clause in clauses:
        clause = clause.strip()
        clause = re.sub(r'^(firstly|secondly|thirdly|next|then|finally)\s+', '', clause, flags=re.I)
        if clause:
            cleaned.append(clause)
    return cleaned

def extract_task_sentences(text):
    doc = nlp(text)
    task_sentences = []
    for sent in doc.sents:
        sent_text = sent.text.strip()
        if is_task_sentence(sent_text):
            for clause in split_into_clauses(sent_text):
                if is_task_sentence(clause):
                    task_sentences.append(clause)
        else:
            parts = [part.strip() for part in sent_text.split(",") if part.strip()]
            for part in parts:
                if is_task_sentence(part):
                    task_sentences.append(part)
    return task_sentences

def categorize(task_sentence):
    tokens = set(task_sentence.lower().split())
    category_scores = {cat: 0 for cat in CATEGORIES}
    for cat, keywords in CATEGORIES.items():
        for keyword in keywords:
            key_tokens = set(keyword.split())
            intersection = tokens.intersection(key_tokens)
            union = tokens.union(key_tokens)
            score = len(intersection) / len(union) if union else 0
            category_scores[cat] += score
    best_cat = max(category_scores, key=category_scores.get)
    if category_scores[best_cat] > 0.1:
        return best_cat
    return "NoCategoryError"

def extraction(text):
    task_sentences = extract_task_sentences(text)
    if not task_sentences:
        return "No tasks mentioned!!"
    structured_tasks = []

    doc = nlp(text)
    default_subject = None
    for token in doc:
        if token.pos_ == "PROPN":
            default_subject = token.text
            break
    for task in task_sentences:
        cat = categorize(task)
        words = task.split()
        if words and words[0].lower() in {"he", "she", "him", "her", "they"} and default_subject:
            words[0] = default_subject
            task = " ".join(words)
        structured_tasks.append({"task": task.strip(), "category": cat})
    return structured_tasks


text = "Rahul wakes up early every day. He goes to college in the morning and comes back at 3 pm. At present, Rahul is outside. He has to buy the snacks for all of us"
text1 = "how is everything and everyone doing today?? I mean is it bring your children to work day? Ha!, just kidding, there is nothing awkward about this"
text2 = "John needs to submit the report by Friday.Please finalize the project plan by next Monday.Sarah will review the presentation tomorrow.The meeting is scheduled for Tuesday."
text3 = "Listen now people, firstly Jagrit will buy the snacks, Vanshika will cook dinner, Darshan is going to clean the room and hall, Atharv will manage everyone."
text4 = "Sohum will do the experiment , but only if vidya does it."
text5 = "Rahul will finish the project by 5pm today."
text6 = "Vishwas will ensure quality in the test reports and double-check all facts before submission."

result = extraction(text)
result1 = extraction(text1)
result2 = extraction(text2)
result3 = extraction(text3)
result4 = extraction(text4)
result5 = extraction(text5)
result6 = extraction(text6)

print(result)
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)
print(result6)
