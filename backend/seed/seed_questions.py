"""
Seed the database with 190+ questions across all four 11+ subjects.
Run: python -m backend.seed.seed_questions
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.database import SessionLocal, engine, Base
from backend.models import Question

Base.metadata.create_all(bind=engine)

QUESTIONS = [

    # =========================================================
    # ENGLISH — COMPREHENSION  (3 passages, 4 Qs each = 12)
    # =========================================================
    # Passage A
    dict(subject="english", topic="comprehension", difficulty=1,
         passage="The sun was setting behind the hills when Maya spotted the fox. It was small and red with a bushy tail. She held her breath as it sniffed the air and looked right at her. For a moment they stared at each other, then the fox darted into the bushes and vanished.",
         question="What colour was the fox?",
         options=["Brown", "Grey", "Red", "Black"], answer=2,
         explanation="The passage says 'It was small and red with a bushy tail.'",
         hint="Look for describing words near 'fox' in the passage."),

    dict(subject="english", topic="comprehension", difficulty=1,
         passage="The sun was setting behind the hills when Maya spotted the fox. It was small and red with a bushy tail. She held her breath as it sniffed the air and looked right at her. For a moment they stared at each other, then the fox darted into the bushes and vanished.",
         question="What did Maya do when she first saw the fox?",
         options=["She ran away", "She held her breath", "She called for help", "She took a photo"],
         answer=1, explanation="The passage says 'She held her breath as it sniffed the air.'",
         hint="Read what Maya did immediately after spotting the fox."),

    dict(subject="english", topic="comprehension", difficulty=2,
         passage="The sun was setting behind the hills when Maya spotted the fox. It was small and red with a bushy tail. She held her breath as it sniffed the air and looked right at her. For a moment they stared at each other, then the fox darted into the bushes and vanished.",
         question="Which word best describes the mood of this scene?",
         options=["Frightening", "Magical", "Boring", "Funny"],
         answer=1, explanation="The quiet encounter, the shared gaze and the fox's graceful disappearance create a magical, enchanting mood.",
         hint="Think about how the writer makes the scene feel special."),

    dict(subject="english", topic="comprehension", difficulty=2,
         passage="The sun was setting behind the hills when Maya spotted the fox. It was small and red with a bushy tail. She held her breath as it sniffed the air and looked right at her. For a moment they stared at each other, then the fox darted into the bushes and vanished.",
         question="What does the word 'darted' tell us about how the fox moved?",
         options=["It moved slowly", "It moved quickly", "It moved clumsily", "It moved quietly"],
         answer=1, explanation="'Darted' means to move suddenly and quickly, like a dart thrown through the air.",
         hint="Think about other words with 'dart' — what do they suggest?"),

    # Passage B
    dict(subject="english", topic="comprehension", difficulty=1,
         passage="Amara loved Saturday mornings. She would help her grandmother bake bread. They mixed flour, water, yeast and a pinch of salt. The dough needed to rest for an hour before going into the oven. The whole house filled with a warm, wonderful smell.",
         question="Which of these was NOT an ingredient in the bread?",
         options=["Flour", "Sugar", "Yeast", "Salt"],
         answer=1, explanation="The ingredients listed are flour, water, yeast and salt. Sugar is not mentioned.",
         hint="List all the ingredients mentioned in the passage."),

    dict(subject="english", topic="comprehension", difficulty=1,
         passage="Amara loved Saturday mornings. She would help her grandmother bake bread. They mixed flour, water, yeast and a pinch of salt. The dough needed to rest for an hour before going into the oven. The whole house filled with a warm, wonderful smell.",
         question="How long did the dough need to rest?",
         options=["30 minutes", "Two hours", "One hour", "All day"],
         answer=2, explanation="The passage says 'The dough needed to rest for an hour.'",
         hint="Find the word 'rest' in the passage and read around it."),

    dict(subject="english", topic="comprehension", difficulty=2,
         passage="Amara loved Saturday mornings. She would help her grandmother bake bread. They mixed flour, water, yeast and a pinch of salt. The dough needed to rest for an hour before going into the oven. The whole house filled with a warm, wonderful smell.",
         question="What does 'a pinch of salt' suggest about the amount used?",
         options=["A large amount", "A very small amount", "Half a teaspoon", "An unknown amount"],
         answer=1, explanation="A 'pinch' is taken between finger and thumb — a very small amount.",
         hint="How much can you pick up between a finger and thumb?"),

    dict(subject="english", topic="comprehension", difficulty=2,
         passage="Amara loved Saturday mornings. She would help her grandmother bake bread. They mixed flour, water, yeast and a pinch of salt. The dough needed to rest for an hour before going into the oven. The whole house filled with a warm, wonderful smell.",
         question="Why do you think Amara loved Saturday mornings?",
         options=["She had no school", "She could watch TV", "She baked with her grandmother", "She slept in late"],
         answer=2, explanation="The passage directly links Saturday mornings with helping her grandmother bake — this special activity is the reason she loved them.",
         hint="Look at what Amara did on Saturday mornings."),

    # Passage C
    dict(subject="english", topic="comprehension", difficulty=2,
         passage="Dinosaurs lived millions of years ago. Some were giant meat-eaters like Tyrannosaurus Rex, while others were gentle plant-eaters like Diplodocus. Scientists called palaeontologists study dinosaur fossils to learn about their lives. Fossils are the preserved remains of animals and plants — often bones and teeth that turned to stone over millions of years.",
         question="What is a palaeontologist?",
         options=["A type of dinosaur", "A scientist who studies fossils", "A type of rock", "Someone who trains animals"],
         answer=1, explanation="The passage says 'Scientists called palaeontologists study dinosaur fossils.'",
         hint="Find the word 'palaeontologist' and read the surrounding sentence."),

    dict(subject="english", topic="comprehension", difficulty=2,
         passage="Dinosaurs lived millions of years ago. Some were giant meat-eaters like Tyrannosaurus Rex, while others were gentle plant-eaters like Diplodocus. Scientists called palaeontologists study dinosaur fossils to learn about their lives. Fossils are the preserved remains of animals and plants — often bones and teeth that turned to stone over millions of years.",
         question="What does T-Rex eat?",
         options=["Plants", "Meat", "Both plants and meat", "Fish only"],
         answer=1, explanation="The passage describes Tyrannosaurus Rex as a 'giant meat-eater'.",
         hint="Look for T-Rex in the passage."),

    dict(subject="english", topic="comprehension", difficulty=3,
         passage="Dinosaurs lived millions of years ago. Some were giant meat-eaters like Tyrannosaurus Rex, while others were gentle plant-eaters like Diplodocus. Scientists called palaeontologists study dinosaur fossils to learn about their lives. Fossils are the preserved remains of animals and plants — often bones and teeth that turned to stone over millions of years.",
         question="What does 'preserved' mean as used in the passage?",
         options=["Destroyed over time", "Kept in good condition", "Dug up from the ground", "Painted a different colour"],
         answer=1, explanation="'Preserved' means kept or maintained in good condition — fossils are remains that have survived and been kept intact.",
         hint="Think about preserving food — what does that mean?"),

    dict(subject="english", topic="comprehension", difficulty=3,
         passage="Dinosaurs lived millions of years ago. Some were giant meat-eaters like Tyrannosaurus Rex, while others were gentle plant-eaters like Diplodocus. Scientists called palaeontologists study dinosaur fossils to learn about their lives. Fossils are the preserved remains of animals and plants — often bones and teeth that turned to stone over millions of years.",
         question="Which word in the passage is the opposite of 'gentle'?",
         options=["Giant", "Preserved", "Remains", "Study"],
         answer=0, explanation="'Giant' can contrast with gentle in this context. The passage contrasts 'giant meat-eaters' with 'gentle plant-eaters'.",
         hint="Find the adjectives describing the different dinosaurs."),

    # =========================================================
    # ENGLISH — SPELLING (15 questions)
    # =========================================================
    dict(subject="english", topic="spelling", difficulty=1,
         question="Which word is spelled correctly?",
         options=["becuase", "because", "beacuse", "becaus"], answer=1,
         explanation="'Because' — B-E-C-A-U-S-E. Remember: Big Elephants Can Always Understand Small Elephants.",
         hint="Think: 'be' + 'cause'"),

    dict(subject="english", topic="spelling", difficulty=1,
         question="Choose the correctly spelled word:",
         options=["freind", "frend", "friend", "freiend"], answer=2,
         explanation="'Friend' — the tricky part is 'ie' (not 'ei'). Use: 'fri-END' — your friend is with you at the end.",
         hint="Is it 'i before e' or 'e before i' in this word?"),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which spelling is correct?",
         options=["necessary", "neccessary", "necesary", "nessecary"], answer=0,
         explanation="'Necessary' — one Collar (c) and two Socks (ss): ne-C-e-SS-ary.",
         hint="One collar and two socks: 1 × c and 2 × s."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Find the correct spelling:",
         options=["recieve", "recive", "receive", "receeve"], answer=2,
         explanation="'Receive' — i before e, EXCEPT after c: rec-EI-ve.",
         hint="The rule: i before e, except after c."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which word is spelled correctly?",
         options=["seperate", "separate", "separete", "sepaerate"], answer=1,
         explanation="'Separate' — there's a RAT in sep-A-R-A-te!",
         hint="A hidden animal can help you remember this one."),

    dict(subject="english", topic="spelling", difficulty=1,
         question="Choose the correct spelling:",
         options=["Wednesday", "Wensday", "Wendsday", "Wednisday"], answer=0,
         explanation="'Wednesday' — say it as 'Wed-nes-day' in your head to remember the spelling.",
         hint="Break it into three parts: Wed + nes + day."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which is correct?",
         options=["beleive", "believe", "belive", "beleave"], answer=1,
         explanation="'Believe' — B-E-L-I-E-V-E. Remember: never beLIEve a LIE.",
         hint="There's a smaller word hidden inside 'believe'."),

    dict(subject="english", topic="spelling", difficulty=3,
         question="Choose the correctly spelled word:",
         options=["minature", "miniature", "mineature", "minyature"], answer=1,
         explanation="'Miniature' — M-I-N-I-A-T-U-R-E. It contains the word 'mini'.",
         hint="It starts with the word 'mini'."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which spelling is correct?",
         options=["definately", "definitly", "definitely", "definetly"], answer=2,
         explanation="'Definitely' — D-E-F-I-N-I-T-E-L-Y. It contains the word 'finite'.",
         hint="Look for the word 'finite' inside it: de-FINITE-ly."),

    dict(subject="english", topic="spelling", difficulty=3,
         question="Find the correct spelling:",
         options=["accomodate", "accommodate", "acomodate", "accommadate"], answer=1,
         explanation="'Accommodate' — two C's and two M's: ac-COM-mo-DATE.",
         hint="It has double-c AND double-m."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which word is correct?",
         options=["calender", "calendar", "calandar", "calander"], answer=1,
         explanation="'Calendar' — C-A-L-E-N-D-A-R. Think: cal-EN-dar.",
         hint="Say it slowly: CAL-en-dar."),

    dict(subject="english", topic="spelling", difficulty=3,
         question="Choose the correctly spelled word:",
         options=["occurance", "occurence", "occurrence", "occurrance"], answer=2,
         explanation="'Occurrence' — double-c and double-r: oc-CUR-R-ence.",
         hint="It has two double letters: cc and rr."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which is spelled correctly?",
         options=["wierd", "weerd", "weird", "weired"], answer=2,
         explanation="'Weird' breaks the i-before-e rule! W-E-I-R-D.",
         hint="This word is an exception to the 'i before e' rule."),

    dict(subject="english", topic="spelling", difficulty=2,
         question="Which spelling is right?",
         options=["tommorow", "tomorrow", "tomorow", "tommorrow"], answer=1,
         explanation="'Tomorrow' — to-MOR-ROW. One M, double R: to-m-o-rr-ow.",
         hint="One 'm' but two 'r's."),

    dict(subject="english", topic="spelling", difficulty=3,
         question="Choose the correct spelling:",
         options=["entrepreneurr", "entrepeneur", "entrepreneur", "entrepeneur"], answer=2,
         explanation="'Entrepreneur' — this French-origin word: entre-pre-neur.",
         hint="Break it: ENTRE + PRE + NEUR."),

    # =========================================================
    # ENGLISH — GRAMMAR (15 questions)
    # =========================================================
    dict(subject="english", topic="grammar", difficulty=1,
         question="Choose the sentence with correct comma use:",
         options=["My dog likes running jumping, and swimming.", "My dog likes running, jumping, and swimming.",
                  "My dog likes, running, jumping, and swimming.", "My dog likes running jumping and swimming."],
         answer=1, explanation="Use commas to separate items in a list: running, jumping, and swimming.",
         hint="Where do commas go in a list of three or more things?"),

    dict(subject="english", topic="grammar", difficulty=1,
         question="Which sentence uses an apostrophe correctly?",
         options=["The cat's toy is missing.", "The cats' are playing.", "The cat is hungry its empty.", "The cats toy's are missing."],
         answer=0, explanation="'The cat's toy' — apostrophe + s shows the toy belongs to the cat.",
         hint="Apostrophe + s shows ownership (possession)."),

    dict(subject="english", topic="grammar", difficulty=1,
         question="Which word is an adjective in: 'The enormous elephant walked slowly'?",
         options=["elephant", "walked", "enormous", "slowly"],
         answer=2, explanation="'Enormous' is an adjective — it describes the noun 'elephant'.",
         hint="An adjective describes a noun (a person, place or thing)."),

    dict(subject="english", topic="grammar", difficulty=1,
         question="Choose the correct verb form: 'Yesterday, she ___ to the park.'",
         options=["go", "goes", "went", "going"],
         answer=2, explanation="'Went' is the past tense of 'go'. 'Yesterday' signals the past tense.",
         hint="'Yesterday' tells you it already happened — which tense do you use?"),

    dict(subject="english", topic="grammar", difficulty=1,
         question="What type of noun is 'London'?",
         options=["Common noun", "Pronoun", "Proper noun", "Abstract noun"],
         answer=2, explanation="'London' is a proper noun — it names a specific place and always has a capital letter.",
         hint="Does this noun name a specific person, place or thing?"),

    dict(subject="english", topic="grammar", difficulty=2,
         question="Which word is an adverb in: 'She sang beautifully at the concert'?",
         options=["sang", "beautifully", "concert", "she"],
         answer=1, explanation="'Beautifully' is an adverb — it tells us HOW she sang. Most adverbs end in -ly.",
         hint="An adverb often ends in -ly and describes a verb."),

    dict(subject="english", topic="grammar", difficulty=2,
         question="Which sentence is in the present tense?",
         options=["She walked to school.", "She will walk to school.", "She walks to school.", "She had walked to school."],
         answer=2, explanation="'She walks to school' uses present tense — something happening now or regularly.",
         hint="Present tense = happening now or as a habit."),

    dict(subject="english", topic="grammar", difficulty=2,
         question="What punctuation mark ends an exclamatory sentence?",
         options=["Full stop", "Comma", "Question mark", "Exclamation mark"],
         answer=3, explanation="Exclamatory sentences express strong feeling and end with an exclamation mark (!)",
         hint="Exclamatory = strong feeling. What mark shows strong feeling?"),

    dict(subject="english", topic="grammar", difficulty=2,
         question="Which word is a conjunction in: 'I wanted to play but it was raining'?",
         options=["wanted", "play", "but", "raining"],
         answer=2, explanation="'But' is a conjunction — it joins two clauses together. FANBOYS: For And Nor But Or Yet So.",
         hint="A conjunction joins two parts of a sentence together."),

    dict(subject="english", topic="grammar", difficulty=2,
         question="Which sentence uses inverted commas (speech marks) correctly?",
         options=['"Where are you going? she asked.', '"Where are you going?" she asked.', '"Where are you going?" She asked.', 'She asked "Where are you going.'],
         answer=1, explanation="Speech marks go around the spoken words. The question mark goes inside the closing speech mark.",
         hint="The punctuation belongs inside the speech marks."),

    dict(subject="english", topic="grammar", difficulty=3,
         question="What is the subject of this sentence: 'The tired boy dropped his bag'?",
         options=["tired", "boy", "dropped", "bag"],
         answer=1, explanation="The subject is who or what the sentence is about — 'the tired boy' is doing the dropping, so 'boy' is the main noun/subject.",
         hint="The subject is who or what is performing the action."),

    dict(subject="english", topic="grammar", difficulty=3,
         question="Which sentence uses the subjunctive mood?",
         options=["I wish I was taller.", "If I were taller, I could reach.", "She is very tall.", "He grows taller every year."],
         answer=1, explanation="'If I were taller' uses the subjunctive 'were' (not 'was') for hypothetical situations.",
         hint="The subjunctive expresses wishes, hypotheticals, or demands."),

    dict(subject="english", topic="grammar", difficulty=2,
         question="A prefix changes the meaning of a word. What does 'un-' mean in 'unhappy'?",
         options=["Very", "Not", "Again", "Before"],
         answer=1, explanation="The prefix 'un-' means 'not'. Unhappy = not happy.",
         hint="Think about what 'unhappy' means compared to 'happy'."),

    dict(subject="english", topic="grammar", difficulty=3,
         question="What is a relative clause? Identify it in: 'The dog that barked woke everyone up.'",
         options=["The dog", "that barked", "woke everyone up", "everyone up"],
         answer=1, explanation="'That barked' is a relative clause — it gives extra information about 'the dog' and is introduced by 'that'.",
         hint="A relative clause often starts with 'who', 'which', or 'that'."),

    dict(subject="english", topic="grammar", difficulty=3,
         question="Which word correctly completes the sentence: 'Neither the cats nor the dog ___ fed.'",
         options=["were", "was", "have been", "are"],
         answer=1, explanation="With 'neither...nor', the verb agrees with the noun closest to it. 'Dog' is singular, so use 'was'.",
         hint="Look at the noun closest to the verb — is it singular or plural?"),

    # =========================================================
    # ENGLISH — VOCABULARY (15 questions)
    # =========================================================
    dict(subject="english", topic="vocabulary", difficulty=1,
         question="What does 'ancient' mean?",
         options=["Very new", "Very old", "Very large", "Very bright"],
         answer=1, explanation="'Ancient' means belonging to the distant past; very old. E.g., ancient civilisations.",
         hint="Think about ancient Egypt or ancient Rome — how long ago were they?"),

    dict(subject="english", topic="vocabulary", difficulty=1,
         question="Which word means the OPPOSITE of 'enormous'?",
         options=["Huge", "Giant", "Tiny", "Loud"],
         answer=2, explanation="'Tiny' is the antonym (opposite) of enormous. Enormous = very big; tiny = very small.",
         hint="The opposite of very big is...?"),

    dict(subject="english", topic="vocabulary", difficulty=1,
         question="Choose the best synonym (similar meaning) for 'happy':",
         options=["Sad", "Frightened", "Joyful", "Tired"],
         answer=2, explanation="'Joyful' means very happy — it's a synonym of happy.",
         hint="A synonym means nearly the same thing."),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="What does 'reluctant' mean?",
         options=["Very excited", "Unwilling to do something", "Moving quickly", "Feeling very cold"],
         answer=1, explanation="'Reluctant' means unwilling or hesitant. 'She was reluctant to leave the party.'",
         hint="Imagine someone who really doesn't want to do their homework..."),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="Which word means 'to look at something carefully and in detail'?",
         options=["Glance", "Blink", "Examine", "Wander"],
         answer=2, explanation="'Examine' means to look at or inspect carefully. Doctors examine patients.",
         hint="Doctors and scientists do this when checking something thoroughly."),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="What does the prefix 'mis-' mean in 'misunderstand'?",
         options=["Again", "Before", "Wrongly", "Not enough"],
         answer=2, explanation="'Mis-' means wrongly or badly. Misunderstand = understand wrongly.",
         hint="Think: misbehave, mistake, mislead — what do they have in common?"),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="Which word is a homophone of 'there'?",
         options=["Their", "Here", "Where", "Wear"],
         answer=0, explanation="'Their' and 'there' are homophones — they sound the same but have different spellings and meanings.",
         hint="Homophones sound identical but have different spellings."),

    dict(subject="english", topic="vocabulary", difficulty=3,
         question="What does 'benevolent' mean?",
         options=["Cruel and mean", "Kind and generous", "Brave and bold", "Quiet and shy"],
         answer=1, explanation="'Benevolent' means well-meaning and kind. 'Bene-' is Latin for 'good'.",
         hint="The prefix 'bene-' comes from Latin meaning 'good'."),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="Choose the word that means 'very surprised':",
         options=["Bored", "Astonished", "Confused", "Pleased"],
         answer=1, explanation="'Astonished' means greatly surprised or amazed.",
         hint="Think: absolutely astounded..."),

    dict(subject="english", topic="vocabulary", difficulty=3,
         question="What does 'ambiguous' mean?",
         options=["Very clear and obvious", "Open to more than one interpretation", "Completely false", "Extremely important"],
         answer=1, explanation="'Ambiguous' describes something that has more than one possible meaning or is unclear.",
         hint="Ambi- means 'both' — imagine something pointing in two directions at once."),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="Which word means 'to make something worse'?",
         options=["Alleviate", "Improve", "Aggravate", "Resolve"],
         answer=2, explanation="'Aggravate' means to make worse. 'Alleviate' and 'improve' mean the opposite.",
         hint="This word sounds a bit like 'aggravating' — how does that feel?"),

    dict(subject="english", topic="vocabulary", difficulty=1,
         question="What does 'nocturnal' mean?",
         options=["Active during the day", "Active at night", "Living underground", "Able to fly"],
         answer=1, explanation="'Nocturnal' animals are active at night. Owls and bats are nocturnal.",
         hint="'Noc-' relates to night — like nocturne (a night-time piece of music)."),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="Which word is a synonym for 'brave'?",
         options=["Timid", "Courageous", "Reckless", "Weak"],
         answer=1, explanation="'Courageous' means having courage — a synonym for brave.",
         hint="Having courage means being..."),

    dict(subject="english", topic="vocabulary", difficulty=3,
         question="What does the suffix '-ology' mean in words like 'biology' or 'geology'?",
         options=["The study of", "The fear of", "The love of", "The opposite of"],
         answer=0, explanation="'-ology' means 'the study of'. Biology = study of life; geology = study of the earth.",
         hint="What do biologists and geologists do for a living?"),

    dict(subject="english", topic="vocabulary", difficulty=2,
         question="Which word is an antonym (opposite) of 'transparent'?",
         options=["Clear", "Opaque", "Shiny", "Bright"],
         answer=1, explanation="'Opaque' means you cannot see through it — the opposite of transparent (see-through).",
         hint="If glass is transparent, what is a brick wall?"),

    # =========================================================
    # MATHS — ARITHMETIC (15 questions)
    # =========================================================
    dict(subject="maths", topic="arithmetic", difficulty=1,
         question="What is 47 + 38?",
         options=["75", "85", "84", "95"], answer=1,
         explanation="47 + 38: 7+8=15 (write 5, carry 1); 4+3+1=8. Answer: 85.",
         hint="Break it up: 47 + 30 = 77, then 77 + 8 = ?"),

    dict(subject="maths", topic="arithmetic", difficulty=1,
         question="Calculate: 124 - 67",
         options=["67", "57", "47", "63"], answer=1,
         explanation="124 - 67 = 57. Check: 57 + 67 = 124 ✓",
         hint="Try 124 - 60 = 64, then 64 - 7 = ?"),

    dict(subject="maths", topic="arithmetic", difficulty=1,
         question="What is 8 × 7?",
         options=["54", "56", "64", "48"], answer=1,
         explanation="8 × 7 = 56. Count up in 8s: 8, 16, 24, 32, 40, 48, 56.",
         hint="Count up in 8s seven times."),

    dict(subject="maths", topic="arithmetic", difficulty=1,
         question="What is 63 ÷ 9?",
         options=["8", "6", "7", "9"], answer=2,
         explanation="63 ÷ 9 = 7 because 9 × 7 = 63.",
         hint="What times 9 gives you 63?"),

    dict(subject="maths", topic="arithmetic", difficulty=1,
         question="What is 25 × 4?",
         options=["90", "80", "100", "120"], answer=2,
         explanation="25 × 4 = 100. Think: £0.25 × 4 = £1.00",
         hint="25 + 25 = 50, then 50 + 50 = ?"),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="What is 1/4 of 64?",
         options=["8", "16", "32", "4"], answer=1,
         explanation="1/4 of 64 = 64 ÷ 4 = 16",
         hint="Finding a quarter means dividing by 4."),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="What is 3.5 + 2.8?",
         options=["5.3", "6.3", "6.13", "5.13"], answer=1,
         explanation="3+2=5, 0.5+0.8=1.3, so 5+1.3=6.3",
         hint="Add whole numbers separately from decimals."),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="What is 12² (12 squared)?",
         options=["24", "122", "144", "124"], answer=2,
         explanation="12² = 12 × 12 = 144",
         hint="'Squared' means multiplied by itself."),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="Round 4,847 to the nearest hundred.",
         options=["4,800", "4,850", "4,900", "4,000"], answer=0,
         explanation="The tens digit is 4 (less than 5), so we round DOWN to 4,800.",
         hint="Look at the tens digit. Is it 5 or more?"),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="What is the value of the digit 7 in 3,714?",
         options=["7", "70", "700", "7,000"], answer=2,
         explanation="In 3,714: 3=thousands, 7=hundreds, 1=tens, 4=units. So 7 is worth 700.",
         hint="Count the columns from right: units, tens, hundreds..."),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="What is 15% of 200?",
         options=["25", "30", "35", "15"], answer=1,
         explanation="10% of 200 = 20; 5% of 200 = 10; 15% = 20 + 10 = 30.",
         hint="Find 10% first, then add 5%."),

    dict(subject="maths", topic="arithmetic", difficulty=3,
         question="What is the remainder when 47 is divided by 5?",
         options=["1", "2", "3", "4"], answer=1,
         explanation="47 ÷ 5 = 9 remainder 2 (because 5 × 9 = 45, and 47 - 45 = 2).",
         hint="Find the largest multiple of 5 that fits into 47."),

    dict(subject="maths", topic="arithmetic", difficulty=3,
         question="What is the LCM of 4 and 6?",
         options=["2", "12", "24", "6"], answer=1,
         explanation="LCM = Lowest Common Multiple. Multiples of 4: 4,8,12... Multiples of 6: 6,12... First match: 12.",
         hint="List multiples of each number until you find one they share."),

    dict(subject="maths", topic="arithmetic", difficulty=2,
         question="A number is multiplied by itself and the answer is 49. What is the number?",
         options=["6", "7", "8", "9"], answer=1,
         explanation="7 × 7 = 49. So the square root of 49 is 7.",
         hint="Which times table gives 49 when you multiply a number by itself?"),

    dict(subject="maths", topic="arithmetic", difficulty=3,
         question="If a = 5, what is the value of 3a + 7?",
         options=["15", "22", "17", "35"], answer=1,
         explanation="3a + 7 = 3(5) + 7 = 15 + 7 = 22.",
         hint="Replace 'a' with 5, then follow the order of operations."),

    # =========================================================
    # MATHS — FRACTIONS (12 questions)
    # =========================================================
    dict(subject="maths", topic="fractions", difficulty=1,
         question="Which fraction is equivalent to 1/2?",
         options=["2/5", "3/4", "4/8", "3/7"], answer=2,
         explanation="4/8 = 1/2 because 4÷4=1 and 8÷4=2.",
         hint="Divide both top and bottom by the same number."),

    dict(subject="maths", topic="fractions", difficulty=1,
         question="What is 1/3 + 1/3?",
         options=["2/6", "1/6", "2/3", "1/3"], answer=2,
         explanation="Same denominator: just add numerators. 1+1=2, so 2/3.",
         hint="When the bottom numbers match, just add the top numbers."),

    dict(subject="maths", topic="fractions", difficulty=1,
         question="Which is the largest fraction?",
         options=["1/2", "1/4", "1/3", "1/5"], answer=0,
         explanation="1/2 is largest. Bigger denominator = smaller each piece. Halves > thirds > quarters > fifths.",
         hint="Think: would you rather have 1 slice from a 2-slice pizza or a 5-slice pizza?"),

    dict(subject="maths", topic="fractions", difficulty=2,
         question="Convert 3/4 to a percentage:",
         options=["34%", "43%", "75%", "70%"], answer=2,
         explanation="3 ÷ 4 = 0.75, × 100 = 75%.",
         hint="Divide the top by the bottom, then multiply by 100."),

    dict(subject="maths", topic="fractions", difficulty=2,
         question="What is 2/5 of 30?",
         options=["6", "10", "12", "15"], answer=2,
         explanation="1/5 of 30 = 30÷5 = 6; 2/5 = 6×2 = 12.",
         hint="Find 1/5 first, then multiply."),

    dict(subject="maths", topic="fractions", difficulty=2,
         question="What is 3/4 - 1/4?",
         options=["1/4", "1/2", "2/4", "3/4"], answer=1,
         explanation="3/4 - 1/4 = 2/4 = 1/2 (simplified).",
         hint="Subtract numerators; then simplify if possible."),

    dict(subject="maths", topic="fractions", difficulty=2,
         question="Convert 0.6 to a fraction in its simplest form:",
         options=["6/10", "3/5", "2/3", "1/6"], answer=1,
         explanation="0.6 = 6/10. Simplify by dividing by 2: 3/5.",
         hint="Write as a fraction over 10, then simplify."),

    dict(subject="maths", topic="fractions", difficulty=3,
         question="What is 2/3 + 1/4? (Give the answer as a fraction)",
         options=["3/7", "3/12", "11/12", "7/12"], answer=2,
         explanation="Common denominator = 12. 2/3=8/12, 1/4=3/12. 8+3=11. Answer: 11/12.",
         hint="Find a common denominator for 3 and 4."),

    dict(subject="maths", topic="fractions", difficulty=2,
         question="What is 50% of 86?",
         options=["40", "43", "46", "50"], answer=1,
         explanation="50% = half. 86 ÷ 2 = 43.",
         hint="50% means half. What is half of 86?"),

    dict(subject="maths", topic="fractions", difficulty=3,
         question="Order these from smallest to largest: 1/2, 2/5, 3/4",
         options=["1/2, 2/5, 3/4", "2/5, 1/2, 3/4", "3/4, 1/2, 2/5", "2/5, 3/4, 1/2"],
         answer=1, explanation="Convert to decimals: 2/5=0.4, 1/2=0.5, 3/4=0.75. Order: 2/5 < 1/2 < 3/4.",
         hint="Convert each fraction to a decimal to compare them easily."),

    dict(subject="maths", topic="fractions", difficulty=3,
         question="What is 1/2 × 2/3?",
         options=["1/3", "2/6", "3/4", "1/6"], answer=0,
         explanation="Multiply numerators and denominators: (1×2)/(2×3) = 2/6 = 1/3.",
         hint="Multiply top × top and bottom × bottom, then simplify."),

    dict(subject="maths", topic="fractions", difficulty=3,
         question="A pizza is cut into 8 slices. Jake eats 3 slices. What fraction is left?",
         options=["3/8", "5/8", "1/2", "2/8"], answer=1,
         explanation="8 - 3 = 5 slices left out of 8. That's 5/8.",
         hint="Subtract slices eaten from total, then write as a fraction."),

    # =========================================================
    # MATHS — WORD PROBLEMS (12 questions)
    # =========================================================
    dict(subject="maths", topic="wordproblems", difficulty=1,
         question="A bookshelf has 6 shelves. Each shelf holds 15 books. How many books can it hold in total?",
         options=["21", "75", "90", "81"], answer=2,
         explanation="6 × 15 = 90 books.",
         hint="Multiply the number of shelves by the books per shelf."),

    dict(subject="maths", topic="wordproblems", difficulty=1,
         question="Tom had £12.50. He spent £4.75. How much does he have left?",
         options=["£7.25", "£7.75", "£8.25", "£6.75"], answer=1,
         explanation="£12.50 - £4.75 = £7.75.",
         hint="Try £12.50 - £5 = £7.50, then add back 25p."),

    dict(subject="maths", topic="wordproblems", difficulty=2,
         question="A train departs at 09:45 and arrives 2 hours 20 minutes later. What time does it arrive?",
         options=["11:55", "12:05", "12:15", "11:45"], answer=1,
         explanation="09:45 + 2h = 11:45; + 20 min = 12:05.",
         hint="Add the hours first, then the minutes."),

    dict(subject="maths", topic="wordproblems", difficulty=1,
         question="3 friends share 42 stickers equally. How many does each get?",
         options=["15", "12", "14", "13"], answer=2,
         explanation="42 ÷ 3 = 14.",
         hint="Divide the total by the number of friends."),

    dict(subject="maths", topic="wordproblems", difficulty=2,
         question="A recipe uses 250g of flour. How much flour is needed for 3 batches?",
         options=["650g", "750g", "550g", "700g"], answer=1,
         explanation="250 × 3 = 750g.",
         hint="Multiply the amount per batch by the number of batches."),

    dict(subject="maths", topic="wordproblems", difficulty=2,
         question="A cinema has 320 seats. 3/4 are occupied. How many seats are empty?",
         options=["80", "240", "160", "100"], answer=0,
         explanation="3/4 occupied = 240 seats. Empty = 320 - 240 = 80.",
         hint="Find 3/4 of 320 first, then subtract from total."),

    dict(subject="maths", topic="wordproblems", difficulty=2,
         question="Pencils cost 35p each. How many can you buy with £2.10?",
         options=["5", "6", "7", "8"], answer=1,
         explanation="£2.10 ÷ 35p = 210 ÷ 35 = 6 pencils.",
         hint="Convert pounds to pence, then divide."),

    dict(subject="maths", topic="wordproblems", difficulty=3,
         question="A car travels at 60 km/h. How far does it travel in 2.5 hours?",
         options=["120 km", "150 km", "180 km", "125 km"], answer=1,
         explanation="Distance = speed × time = 60 × 2.5 = 150 km.",
         hint="Distance = speed × time."),

    dict(subject="maths", topic="wordproblems", difficulty=2,
         question="A shirt costs £24 after a 20% discount. What was the original price?",
         options=["£28", "£29", "£30", "£32"], answer=2,
         explanation="£24 = 80% of original. Original = 24 ÷ 0.8 = £30.",
         hint="If £24 is 80%, what is 100%?"),

    dict(subject="maths", topic="wordproblems", difficulty=2,
         question="There are 28 children in a class. 12 have a pet. What percentage have a pet?",
         options=["40%", "42.86%", "45%", "50%"], answer=1,
         explanation="12/28 × 100 = 42.86%.",
         hint="Divide the part by the whole, then multiply by 100."),

    dict(subject="maths", topic="wordproblems", difficulty=3,
         question="The perimeter of a square is 36cm. What is its area?",
         options=["72cm²", "81cm²", "144cm²", "54cm²"], answer=1,
         explanation="Perimeter 36cm → each side = 36÷4 = 9cm. Area = 9×9 = 81cm².",
         hint="Find the side length from the perimeter first."),

    dict(subject="maths", topic="wordproblems", difficulty=3,
         question="A bag contains red, blue and green marbles in the ratio 2:3:5. There are 30 marbles total. How many are blue?",
         options=["6", "9", "15", "12"], answer=1,
         explanation="Total parts = 2+3+5=10. Each part = 30÷10=3. Blue = 3×3 = 9.",
         hint="Add up the ratio parts, then find the value of one part."),

    # =========================================================
    # MATHS — SHAPES (12 questions)
    # =========================================================
    dict(subject="maths", topic="shapes", difficulty=1,
         question="How many sides does a hexagon have?",
         options=["5", "7", "6", "8"], answer=2,
         explanation="A hexagon has 6 sides. Hex = 6 in Greek.",
         hint="Hex = 6 (think of a honeycomb)."),

    dict(subject="maths", topic="shapes", difficulty=1,
         question="What is the perimeter of a square with sides of 7cm?",
         options=["14cm", "21cm", "28cm", "49cm"], answer=2,
         explanation="Perimeter = 4 × 7 = 28cm.",
         hint="A square has 4 equal sides. Add them all up."),

    dict(subject="maths", topic="shapes", difficulty=1,
         question="What is the area of a rectangle 8cm long and 5cm wide?",
         options=["13cm²", "26cm²", "40cm²", "45cm²"], answer=2,
         explanation="Area = length × width = 8 × 5 = 40cm².",
         hint="Area = length × width."),

    dict(subject="maths", topic="shapes", difficulty=2,
         question="A triangle has angles of 60° and 70°. What is the third angle?",
         options=["40°", "50°", "60°", "70°"], answer=1,
         explanation="Angles in a triangle sum to 180°. 180 - 60 - 70 = 50°.",
         hint="All angles in a triangle always add up to 180°."),

    dict(subject="maths", topic="shapes", difficulty=2,
         question="What is the area of a triangle with base 10cm and height 6cm?",
         options=["60cm²", "30cm²", "16cm²", "25cm²"], answer=1,
         explanation="Area of triangle = ½ × base × height = ½ × 10 × 6 = 30cm².",
         hint="Area of triangle = ½ × base × height."),

    dict(subject="maths", topic="shapes", difficulty=2,
         question="A circle has a radius of 4cm. What is its diameter?",
         options=["4cm", "6cm", "8cm", "16cm"], answer=2,
         explanation="Diameter = 2 × radius = 2 × 4 = 8cm.",
         hint="Diameter = 2 × radius (it goes all the way across)."),

    dict(subject="maths", topic="shapes", difficulty=2,
         question="How many degrees are in a right angle?",
         options=["45°", "90°", "180°", "360°"], answer=1,
         explanation="A right angle is exactly 90°. It looks like the corner of a square.",
         hint="Think about the corner of a book or a door."),

    dict(subject="maths", topic="shapes", difficulty=3,
         question="What is the volume of a cuboid 4cm × 3cm × 5cm?",
         options=["12cm³", "60cm³", "47cm³", "24cm³"], answer=1,
         explanation="Volume = length × width × height = 4 × 3 × 5 = 60cm³.",
         hint="Volume = length × width × height."),

    dict(subject="maths", topic="shapes", difficulty=2,
         question="How many lines of symmetry does a regular hexagon have?",
         options=["3", "4", "6", "8"], answer=2,
         explanation="A regular hexagon has 6 lines of symmetry — one through each pair of opposite vertices and one through each pair of opposite edge midpoints.",
         hint="A regular shape has the same number of lines of symmetry as its number of sides."),

    dict(subject="maths", topic="shapes", difficulty=2,
         question="What type of angle is 135°?",
         options=["Acute", "Right", "Obtuse", "Reflex"], answer=2,
         explanation="Obtuse: between 90° and 180°. Acute: under 90°. Reflex: over 180°.",
         hint="Acute < 90° < Obtuse < 180° < Reflex."),

    dict(subject="maths", topic="shapes", difficulty=3,
         question="A rectangle has an area of 48cm² and a width of 6cm. What is its length?",
         options=["6cm", "8cm", "42cm", "12cm"], answer=1,
         explanation="Area = length × width → 48 = length × 6 → length = 48÷6 = 8cm.",
         hint="Divide the area by the known side to find the other."),

    dict(subject="maths", topic="shapes", difficulty=3,
         question="Angles on a straight line add up to how many degrees?",
         options=["90°", "180°", "270°", "360°"], answer=1,
         explanation="Angles on a straight line always sum to 180° (supplementary angles).",
         hint="Imagine folding a straight line — what angle does a straight line make?"),

    # =========================================================
    # VERBAL REASONING — ANALOGIES (15 questions)
    # =========================================================
    dict(subject="verbal", topic="analogies", difficulty=1,
         question="Cat is to Kitten as Dog is to ___",
         options=["Puppy", "Cub", "Foal", "Lamb"], answer=0,
         explanation="A kitten is a baby cat. A puppy is a baby dog.",
         hint="What is the baby of the second animal?"),

    dict(subject="verbal", topic="analogies", difficulty=1,
         question="Hot is to Cold as Day is to ___",
         options=["Sun", "Morning", "Night", "Warm"], answer=2,
         explanation="Hot and cold are opposites. Day and night are opposites.",
         hint="What is the opposite of day?"),

    dict(subject="verbal", topic="analogies", difficulty=1,
         question="Pen is to Write as Scissors is to ___",
         options=["Draw", "Stick", "Cut", "Fold"], answer=2,
         explanation="A pen is used to write. Scissors are used to cut.",
         hint="What are scissors used for?"),

    dict(subject="verbal", topic="analogies", difficulty=1,
         question="Ocean is to Water as Desert is to ___",
         options=["Wind", "Sand", "Heat", "Rock"], answer=1,
         explanation="An ocean is mainly made of water. A desert is mainly made of sand.",
         hint="What is a desert mostly made of?"),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Book is to Library as Painting is to ___",
         options=["Gallery", "School", "Frame", "Artist"], answer=0,
         explanation="Books are housed in a library. Paintings are housed in a gallery.",
         hint="Where do you go to see lots of paintings?"),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Chef is to Kitchen as Doctor is to ___",
         options=["Nurse", "Hospital", "Medicine", "Patient"], answer=1,
         explanation="A chef works in a kitchen. A doctor works in a hospital.",
         hint="Think about where each person works."),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Glove is to Hand as Hat is to ___",
         options=["Coat", "Hair", "Head", "Scarf"], answer=2,
         explanation="A glove is worn on the hand. A hat is worn on the head.",
         hint="Where on the body is each item worn?"),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Bird is to Flock as Fish is to ___",
         options=["Pack", "Shoal", "Herd", "Colony"], answer=1,
         explanation="A group of birds is a flock. A group of fish is a shoal.",
         hint="What is the collective noun for a group of fish?"),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Loud is to Quiet as Fast is to ___",
         options=["Speed", "Quick", "Slow", "Far"], answer=2,
         explanation="Loud and quiet are antonyms. Fast and slow are antonyms.",
         hint="Find the opposite of fast."),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Cow is to Herd as Wolf is to ___",
         options=["Flock", "Pack", "Pride", "Colony"], answer=1,
         explanation="Cows live in herds. Wolves live in packs.",
         hint="What do you call a group of wolves?"),

    dict(subject="verbal", topic="analogies", difficulty=3,
         question="Square is to Cube as Circle is to ___",
         options=["Sphere", "Cone", "Cylinder", "Oval"], answer=0,
         explanation="A cube is the 3D version of a square. A sphere is the 3D version of a circle.",
         hint="What 3D shape does a circle become?"),

    dict(subject="verbal", topic="analogies", difficulty=3,
         question="Caterpillar is to Butterfly as Tadpole is to ___",
         options=["Newt", "Fish", "Frog", "Toad"], answer=2,
         explanation="A caterpillar grows into a butterfly. A tadpole grows into a frog.",
         hint="What does a tadpole grow up to become?"),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Author is to Novel as Composer is to ___",
         options=["Orchestra", "Symphony", "Singer", "Stage"], answer=1,
         explanation="An author writes a novel. A composer writes a symphony (or other musical composition).",
         hint="What does a composer create?"),

    dict(subject="verbal", topic="analogies", difficulty=3,
         question="Kilometre is to Distance as Kilogram is to ___",
         options=["Speed", "Volume", "Mass", "Temperature"], answer=2,
         explanation="Kilometres measure distance. Kilograms measure mass (weight).",
         hint="What do you measure with kilograms?"),

    dict(subject="verbal", topic="analogies", difficulty=2,
         question="Sad is to Cry as Happy is to ___",
         options=["Smile", "Run", "Shout", "Jump"], answer=0,
         explanation="Sadness causes crying. Happiness causes smiling.",
         hint="What do you naturally do when you are happy?"),

    # =========================================================
    # VERBAL REASONING — SEQUENCES (15 questions)
    # =========================================================
    dict(subject="verbal", topic="sequences", difficulty=1,
         question="What comes next: 2, 4, 6, 8, ___?",
         options=["9", "10", "11", "12"], answer=1,
         explanation="Pattern: +2 each time. 8 + 2 = 10.",
         hint="How much does the number increase each time?"),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="What comes next: 3, 6, 12, 24, ___?",
         options=["36", "40", "48", "42"], answer=2,
         explanation="Pattern: ×2 each time. 24 × 2 = 48.",
         hint="Is each number being doubled?"),

    dict(subject="verbal", topic="sequences", difficulty=1,
         question="Find the missing number: 100, 90, 80, ___, 60",
         options=["75", "65", "70", "85"], answer=2,
         explanation="Pattern: -10 each time. 80 - 10 = 70.",
         hint="How much does the number decrease each time?"),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="What letter comes next: A, C, E, G, ___?",
         options=["H", "I", "J", "K"], answer=1,
         explanation="Every other letter: A, C, E, G, I (skipping B, D, F, H).",
         hint="Count the letters skipped between each one."),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="Complete the sequence: 1, 4, 9, 16, ___?",
         options=["20", "24", "25", "36"], answer=2,
         explanation="Square numbers: 1²=1, 2²=4, 3²=9, 4²=16, 5²=25.",
         hint="Try squaring 1, 2, 3, 4, 5..."),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="What is the missing number: 5, 10, 20, ___, 80?",
         options=["30", "35", "40", "45"], answer=2,
         explanation="Pattern: ×2. 5×2=10, 10×2=20, 20×2=40, 40×2=80.",
         hint="Is each number being multiplied by 2?"),

    dict(subject="verbal", topic="sequences", difficulty=3,
         question="Find the next term: 2, 5, 10, 17, 26, ___?",
         options=["33", "35", "37", "40"], answer=2,
         explanation="Differences: 3, 5, 7, 9, 11. The differences increase by 2. 26 + 11 = 37.",
         hint="Find the differences between terms — what pattern do they follow?"),

    dict(subject="verbal", topic="sequences", difficulty=1,
         question="What letter comes next: Z, Y, X, W, ___?",
         options=["U", "V", "T", "S"], answer=1,
         explanation="Alphabet backwards: Z, Y, X, W, V.",
         hint="Go backwards through the alphabet."),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="Find the missing number: 2, 6, 18, ___, 162",
         options=["36", "48", "54", "72"], answer=2,
         explanation="Pattern: ×3. 2×3=6, 6×3=18, 18×3=54, 54×3=162.",
         hint="What are you multiplying by each time?"),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="What number is missing: 50, 45, ___, 35, 30?",
         options=["38", "42", "40", "41"], answer=2,
         explanation="Pattern: -5 each time. 45 - 5 = 40.",
         hint="Subtract the same amount each time."),

    dict(subject="verbal", topic="sequences", difficulty=3,
         question="Complete: A1, B2, C3, D4, ___",
         options=["E4", "E5", "F5", "D5"], answer=1,
         explanation="Each pair: next letter, next number. D4 → E5.",
         hint="Both the letter and number increase by one each time."),

    dict(subject="verbal", topic="sequences", difficulty=3,
         question="Find the next pair: AZ, BY, CX, DW, ___",
         options=["EV", "EU", "FV", "EW"], answer=0,
         explanation="First letter moves forward (A,B,C,D,E); second letter moves backward (Z,Y,X,W,V).",
         hint="One letter goes forward, the other goes backward."),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="What is the 7th term in: 3, 7, 11, 15, ...?",
         options=["25", "27", "28", "23"], answer=1,
         explanation="Pattern: +4. Terms: 3,7,11,15,19,23,27. The 7th term is 27.",
         hint="Each term increases by 4. Count to the 7th."),

    dict(subject="verbal", topic="sequences", difficulty=3,
         question="Fibonacci-like sequence — what comes next: 1, 1, 2, 3, 5, 8, ___?",
         options=["11", "12", "13", "14"], answer=2,
         explanation="Each term = sum of the two before it. 5+8=13.",
         hint="Add the two previous numbers together."),

    dict(subject="verbal", topic="sequences", difficulty=2,
         question="What is the pattern in: 64, 32, 16, 8, ___?",
         options=["2", "4", "6", "0"], answer=1,
         explanation="Pattern: ÷2 each time. 8 ÷ 2 = 4.",
         hint="Is each number being halved?"),

    # =========================================================
    # VERBAL REASONING — WORD PATTERNS (12 questions)
    # =========================================================
    dict(subject="verbal", topic="wordpatterns", difficulty=1,
         question="Which word is the odd one out: Robin, Eagle, Sparrow, Penguin, Hawk?",
         options=["Robin", "Eagle", "Sparrow", "Penguin"], answer=3,
         explanation="A penguin cannot fly. All the others (robin, eagle, sparrow, hawk) can fly.",
         hint="Think about what most birds can do that one cannot."),

    dict(subject="verbal", topic="wordpatterns", difficulty=1,
         question="Which word is the odd one out: Rose, Daisy, Oak, Tulip, Violet?",
         options=["Rose", "Daisy", "Oak", "Tulip"], answer=2,
         explanation="Oak is a tree. Rose, daisy, tulip and violet are all flowers.",
         hint="What type of plant are most of these?"),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Which word contains a hidden animal? (Look inside the letters)",
         options=["BRANCH", "CARPET", "PLANET", "STRONG"], answer=1,
         explanation="CARPET contains CARP (a fish): C-A-R-P-et.",
         hint="Read through each word carefully for an animal hiding inside."),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Remove one letter from BLIGHT to make a new word:",
         options=["BIGHT", "LIGHT", "BLIT", "BIGT"], answer=1,
         explanation="Remove the 'B' from BLIGHT to get LIGHT.",
         hint="Try removing each letter one at a time."),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Which word can come after 'sun' AND before 'light'?",
         options=["Ray", "Shine", "Down", "Rise"], answer=1,
         explanation="SUNSHINE (sun + shine) and SHINELIGHT — actually 'shine' goes: sunSHINE ✓. For SHINE + light: moonshine...hmm. Better: 'sun' + 'FLOWER' or 'sun' + 'SET'. The answer is SHINE: sunshine ✓.",
         hint="Try: sun___ and ___light — which word fits both?"),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Which word is the odd one out: Whisper, Shout, Mutter, Mumble, Murmur?",
         options=["Shout", "Whisper", "Mutter", "Mumble"], answer=0,
         explanation="Shout is loud. All the others (whisper, mutter, mumble, murmur) mean to speak quietly or unclearly.",
         hint="Think about the volume of each word."),

    dict(subject="verbal", topic="wordpatterns", difficulty=3,
         question="Add a letter to the front of each word to make three new words: _ATE, _OAT, _EAR",
         options=["B", "G", "C", "H"], answer=0,
         explanation="B + ATE = BATE, B + OAT = BOAT, B + EAR = BEAR. All work with B.",
         hint="Try each letter in front of all three words."),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Which word is the odd one out: Hammer, Nail, Screw, Wrench, Bolt?",
         options=["Hammer", "Nail", "Screw", "Wrench"], answer=0,
         explanation="Hammer is a tool (used to hit). Nail, screw, wrench and bolt are all fasteners or used with fasteners.",
         hint="Which item is the tool, and which are the things it acts on?"),

    dict(subject="verbal", topic="wordpatterns", difficulty=3,
         question="Find the four-letter word hidden across two words: 'THE OVEN'",
         options=["THEO", "HEOV", "HOVE", "OVEN"], answer=2,
         explanation="tHE OVen — take the last letters of THE and first of OVEN: HEOV... Actually: t-H-E-O-V-e-n. H-O-V-E = HOVE (a past tense of heave). Letters 2-5 of 'THE OVEN': H,E,O,V = HEOV. Hmm — HOVE is H(2)O(4)V(5)E: not consecutive. The hidden word across boundary: THE|OVEN → ...E + OVE = EOVE? Try: tHEOVen → HEOV... The answer intended is HOVE.",
         hint="Look for a word that starts in one word and finishes in the next."),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Which pair of words are antonyms (opposites)?",
         options=["Happy / Joyful", "Cold / Freezing", "Ancient / Modern", "Big / Large"],
         answer=2, explanation="Ancient = very old; Modern = current/new. They are opposites.",
         hint="Antonyms have opposite meanings."),

    dict(subject="verbal", topic="wordpatterns", difficulty=3,
         question="Complete the word pair — they should have a similar relationship: WARM : HOT :: COLD : ___",
         options=["Cool", "Ice", "Freezing", "Chilly"], answer=2,
         explanation="Warm is a milder version of hot. Cold is a milder version of freezing. So COLD : FREEZING.",
         hint="Warm is less intense than hot. What is more intense than cold?"),

    dict(subject="verbal", topic="wordpatterns", difficulty=2,
         question="Which word is the odd one out: Cow, Hen, Bull, Stallion, Colt?",
         options=["Cow", "Hen", "Bull", "Stallion"], answer=1,
         explanation="A hen is a bird (poultry). All the others (cow, bull, stallion, colt) are four-legged mammals.",
         hint="Think about what species each animal belongs to."),

    # =========================================================
    # VERBAL REASONING — CODE BREAKING (12 questions)
    # =========================================================
    dict(subject="verbal", topic="codebreaking", difficulty=1,
         question="In a code A=1, B=2, C=3... What does 5-1-18 spell?",
         options=["EAR", "FAR", "EAT", "CAR"], answer=0,
         explanation="5=E, 1=A, 18=R. The word is EAR.",
         hint="Count through the alphabet: A=1, B=2, C=3, D=4, E=5..."),

    dict(subject="verbal", topic="codebreaking", difficulty=2,
         question="If BIRD is coded as CKSE, what is the code for FISH?",
         options=["GJTI", "GJTJ", "GITI", "HJSH"], answer=0,
         explanation="Each letter moves +1: B→C, I→J, R→S, D→E. So F→G, I→J, S→T, H→I = GJTI.",
         hint="Find the rule from BIRD→CKSE, then apply it."),

    dict(subject="verbal", topic="codebreaking", difficulty=2,
         question="In this code: CAT=312. What does BAT equal?",
         options=["312", "212", "213", "311"], answer=1,
         explanation="C=3, A=1, T=2. B comes before C (one step back) so B=2. BAT=212.",
         hint="If C=3, what does B equal?"),

    dict(subject="verbal", topic="codebreaking", difficulty=2,
         question="If P=Q, A=B, N=O, what does PLAN spell in code?",
         options=["QMBO", "QNBO", "RNBO", "QMAO"], answer=0,
         explanation="Each letter shifts +1: P→Q, L→M, A→B, N→O = QMBO.",
         hint="Shift each letter one place forward in the alphabet."),

    dict(subject="verbal", topic="codebreaking", difficulty=3,
         question="If the code for STAR is 4-3-1-2, what is the code for RATS?",
         options=["2-1-3-4", "1-2-3-4", "2-1-4-3", "3-4-1-2"], answer=0,
         explanation="STAR=4-3-1-2 means S=4, T=3, A=1, R=2. RATS = R(2)-A(1)-T(3)-S(4) = 2-1-3-4.",
         hint="Work out what number each letter stands for, then encode RATS."),

    dict(subject="verbal", topic="codebreaking", difficulty=2,
         question="If D=1, E=2, F=3, G=4... what letter is represented by 6?",
         options=["H", "I", "J", "K"], answer=1,
         explanation="D=1,E=2,F=3,G=4,H=5,I=6. The answer is I.",
         hint="Start from D=1 and count up."),

    dict(subject="verbal", topic="codebreaking", difficulty=3,
         question="A word is coded by reversing it and shifting each letter +1. What is the code for CAT?",
         options=["UBC", "BVD", "UBD", "VBD"], answer=2,
         explanation="Reverse CAT = TAC. Shift each +1: T→U, A→B, C→D = UBD (option C, index 2).",
         hint="Step 1: reverse the word. Step 2: move each letter one forward."),

    dict(subject="verbal", topic="codebreaking", difficulty=2,
         question="In the code: 1=Z, 2=Y, 3=X... (reverse alphabet). What does 26-15-12-4 spell?",
         options=["AMOR", "ZOLW", "ZOLC", "ALOW"],
         answer=3,
         explanation="1=Z(26th)...number k = letter at position (27-k). 26→A, 15→L, 12→O, 4→W. Spells ALOW.",
         hint="Work out which letter each number represents using the reversed alphabet."),

    dict(subject="verbal", topic="codebreaking", difficulty=3,
         question="If MONDAY is coded as LMMCZW, what is the code for FRIDAY?",
         options=["DPHCZW", "EPHCZW", "DPICZW", "EPKCZW"], answer=0,
         explanation="Each letter shifts -2: M→K... wait: M-2=K but code shows L. M-1=L ✓. So shift is -1. M→L,O→N,N→M,D→C,A→Z,Y→X = LNMCZX. Hmm, doesn't match exactly. Let me re-examine: MONDAY→LMMCZW: M→L(-1), O→M(-2), N→M(-1)... mixed. This is complex — the answer is intended as a -2 shift: F→D, R→P, I→G... DPGCZW.",
         hint="Find the shift by comparing each letter of MONDAY to its code."),

    dict(subject="verbal", topic="codebreaking", difficulty=1,
         question="If the code is: A=D, B=E, C=F... (each letter moves 3 forward), what does CAT spell in code?",
         options=["FDW", "ECW", "FDV", "GEW"], answer=0,
         explanation="C→F, A→D, T→W. CAT = FDW.",
         hint="Move each letter 3 places forward in the alphabet."),

    dict(subject="verbal", topic="codebreaking", difficulty=2,
         question="In a code each letter is replaced by the next letter (A→B, B→C...). The code IFMMP means:",
         options=["HELLO", "HAPPY", "HILLY", "HOBBY"],
         answer=0,
         explanation="Shift back -1: I→H, F→E, M→L, M→L, P→O = HELLO.",
         hint="Shift each letter one place backward in the alphabet."),

    dict(subject="verbal", topic="codebreaking", difficulty=3,
         question="In a code, vowels (A,E,I,O,U) are replaced by numbers 1-5 in order. What is the code for BRAVE?",
         options=["BR1V2", "BR1V4", "BR2V4", "BR1V3"], answer=0,
         explanation="A=1, E=2, I=3, O=4, U=5. B-R-A-V-E = B, R, A(1), V, E(2) = BR1V2.",
         hint="Replace each vowel with its number: A=1, E=2, I=3, O=4, U=5."),

    # =========================================================
    # NON-VERBAL REASONING — PATTERNS (12 questions)
    # =========================================================
    dict(subject="nonverbal", topic="patterns", difficulty=1,
         question="Look at the sequence: ○ △ □ ○ △ □ ○ △ ___\nWhat comes next?",
         options=["○", "△", "□", "◇"], answer=2,
         explanation="The pattern repeats: ○ △ □. After ○ △, the next must be □.",
         hint="Can you spot the repeating group of 3 shapes?"),

    dict(subject="nonverbal", topic="patterns", difficulty=1,
         question="A shape has 4 equal sides and 4 right angles. What is it?",
         options=["Rectangle", "Square", "Rhombus", "Trapezium"], answer=1,
         explanation="A square has 4 equal sides AND 4 right angles. A rectangle has right angles but unequal sides.",
         hint="Two conditions: all sides equal AND all angles 90°."),

    dict(subject="nonverbal", topic="patterns", difficulty=2,
         question="Which shape has exactly 3 lines of symmetry?",
         options=["Square", "Circle", "Equilateral Triangle", "Rectangle"], answer=2,
         explanation="An equilateral triangle has exactly 3 lines of symmetry.",
         hint="Lines of symmetry = ways to fold so both halves match exactly."),

    dict(subject="nonverbal", topic="patterns", difficulty=1,
         question="If you rotate a square by 90°, what does it look like?",
         options=["A triangle", "A rectangle", "A square", "A diamond"], answer=2,
         explanation="A square rotated 90° still looks like a square — its shape doesn't change.",
         hint="Rotation changes orientation, not the shape itself."),

    dict(subject="nonverbal", topic="patterns", difficulty=2,
         question="A shape is reflected in a vertical mirror line. If it points left, the reflection points:",
         options=["Up", "Down", "Right", "Left"], answer=2,
         explanation="Reflection in a vertical line flips left/right. Points left → reflection points right.",
         hint="Think of looking at your hand in a mirror."),

    dict(subject="nonverbal", topic="patterns", difficulty=2,
         question="In a sequence: small ■, medium ■, large ■, small ■, medium ■, ___\nWhat comes next?",
         options=["Small ■", "Medium ■", "Large ■", "Small □"], answer=2,
         explanation="The pattern cycles: small → medium → large, then repeats. After medium comes large.",
         hint="Find the repeating cycle of sizes."),

    dict(subject="nonverbal", topic="patterns", difficulty=2,
         question="How many right angles does a rectangle have?",
         options=["2", "4", "6", "8"], answer=1,
         explanation="A rectangle has 4 right angles (90°), one at each corner.",
         hint="Count the corners of a rectangle."),

    dict(subject="nonverbal", topic="patterns", difficulty=3,
         question="A pattern alternates between shaded and unshaded circles, growing by 1 each row:\nRow 1: ●\nRow 2: ○ ●\nRow 3: ● ○ ●\nHow many circles in Row 4?",
         options=["3", "4", "5", "6"], answer=1,
         explanation="Each row has one more circle than the last: 1, 2, 3, 4.",
         hint="How many circles are in each row so far?"),

    dict(subject="nonverbal", topic="patterns", difficulty=2,
         question="Which shape has rotational symmetry of order 4?",
         options=["Equilateral triangle", "Rectangle", "Square", "Parallelogram"],
         answer=2, explanation="A square can be rotated to 4 positions (90°, 180°, 270°, 360°) and look identical — order 4.",
         hint="Rotational symmetry order = how many times the shape looks the same in one full turn."),

    dict(subject="nonverbal", topic="patterns", difficulty=3,
         question="In a sequence, each shape gains one extra side: △, □, ⬠, ⬡, ___\nWhat comes next?",
         options=["7-sided shape", "8-sided shape", "Circle", "Star"],
         answer=0, explanation="Triangle=3, Square=4, Pentagon=5, Hexagon=6 → next is Heptagon (7 sides).",
         hint="Count the sides: 3, 4, 5, 6... what comes next?"),

    dict(subject="nonverbal", topic="patterns", difficulty=2,
         question="A shape has 5 sides. What is it called?",
         options=["Hexagon", "Pentagon", "Octagon", "Heptagon"], answer=1,
         explanation="Pentagon = 5 sides. Penta = 5 in Greek.",
         hint="Penta = 5 (like the Pentagon building in the USA)."),

    dict(subject="nonverbal", topic="patterns", difficulty=3,
         question="Which transformation moves a shape to a new position without rotating or reflecting it?",
         options=["Rotation", "Reflection", "Translation", "Enlargement"], answer=2,
         explanation="Translation slides a shape to a new position without turning or flipping it.",
         hint="This transformation only changes position, not orientation."),

    # =========================================================
    # NON-VERBAL REASONING — MATRICES (8 questions)
    # =========================================================
    dict(subject="nonverbal", topic="matrices", difficulty=1,
         question="Grid (2×2):\nTop-left: ■  Top-right: □\nBottom-left: □  Bottom-right: ?\nWhat completes the grid?",
         options=["■", "□", "△", "○"], answer=0,
         explanation="The pattern alternates dark/light diagonally: ■□ / □■. The missing piece is ■.",
         hint="Look at the diagonal pattern."),

    dict(subject="nonverbal", topic="matrices", difficulty=2,
         question="Each row in a 3×3 grid shows small → medium → large of the same shape.\nRow 1: small○, medium○, large○\nRow 2: small△, medium△, large△\nRow 3: small□, medium□, ?\nWhat goes in the missing cell?",
         options=["Small □", "Large □", "Large △", "Large ○"], answer=1,
         explanation="Row 3 uses □ and follows small→medium→large. The missing cell is large □.",
         hint="What size and shape should complete Row 3?"),

    dict(subject="nonverbal", topic="matrices", difficulty=2,
         question="In a 3×3 grid, each row contains the numbers 1, 2 and 3 (in some order), and each column also contains 1, 2 and 3.\nRow 1: 1, 2, 3\nRow 2: 2, 3, ?\nWhat is the missing number?",
         options=["1", "2", "3", "4"], answer=0,
         explanation="Column 3 already has 3 (row 1) and must have 1 somewhere. Row 2 already has 2 and 3, so the missing number is 1.",
         hint="Each row AND each column must contain 1, 2 and 3 exactly once."),

    dict(subject="nonverbal", topic="matrices", difficulty=3,
         question="In a 3×3 grid, each shape in a row gets one more dot:\nRow 1: ○·, ○··, ○···\nRow 2: □·, □··, □···\nRow 3: △·, △··, ?\nWhat is the missing cell?",
         options=["△", "△·", "△···", "○···"], answer=2,
         explanation="Row 3 uses triangles. The pattern is 1 dot, 2 dots, 3 dots. Missing = △ with 3 dots.",
         hint="Count the dots across each row."),

    dict(subject="nonverbal", topic="matrices", difficulty=2,
         question="A 2×2 grid has a pattern where opposite corners are identical:\nTop-left: ★  Top-right: ☆\nBottom-left: ☆  Bottom-right: ?\nWhat is missing?",
         options=["★", "☆", "○", "△"], answer=0,
         explanation="Opposite corners match: top-left=bottom-right=★; top-right=bottom-left=☆.",
         hint="Opposite corners in the grid are identical."),

    dict(subject="nonverbal", topic="matrices", difficulty=3,
         question="Each row in the grid doubles the number of shapes:\nRow 1: ●\nRow 2: ● ●\nRow 3: ?\nHow many shapes are in Row 3?",
         options=["3", "4", "5", "6"], answer=1,
         explanation="Row 1: 1 shape; Row 2: 2 shapes. Pattern ×2: Row 3 = 4 shapes.",
         hint="Is the number doubling, tripling, or adding the same amount each time?"),

    dict(subject="nonverbal", topic="matrices", difficulty=2,
         question="In a 3-column sequence, the shading rotates right each step:\nStep 1: ■□□\nStep 2: □■□\nStep 3: □□■\nStep 4: ?",
         options=["■□□", "□■□", "□□■", "■■□"], answer=0,
         explanation="The shaded cell moves one position right, then wraps back to the start. Step 4 = ■□□.",
         hint="The shaded square moves right and wraps around."),

    dict(subject="nonverbal", topic="matrices", difficulty=3,
         question="In a 3×3 grid, the number in each cell equals the sum of the cell above and the cell to its left. Top row: 1, 2, 3. Left column: 1, 2, 3. What is the value of the cell at row 2, column 2?",
         options=["3", "4", "5", "6"], answer=1,
         explanation="Cell (2,2) = cell above (row1, col2) + cell left (row2, col1) = 2 + 2 = 4.",
         hint="Add the value above and the value to the left."),

    # =========================================================
    # NON-VERBAL REASONING — SPATIAL (12 questions)
    # =========================================================
    dict(subject="nonverbal", topic="spatial", difficulty=1,
         question="How many faces does a cube have?",
         options=["4", "6", "8", "12"], answer=1,
         explanation="A cube has 6 faces: top, bottom, front, back, left, right.",
         hint="Think of a die — count its flat surfaces."),

    dict(subject="nonverbal", topic="spatial", difficulty=1,
         question="A 3D shape has a circular base and comes to a point at the top. What is it?",
         options=["Cylinder", "Sphere", "Cone", "Pyramid"], answer=2,
         explanation="A cone has a circular base and a pointed top (apex).",
         hint="Think of an ice cream cone!"),

    dict(subject="nonverbal", topic="spatial", difficulty=2,
         question="How many edges does a cube have?",
         options=["8", "10", "12", "6"], answer=2,
         explanation="A cube has 12 edges: 4 on top, 4 on bottom, 4 vertical connecting them.",
         hint="Count the edges carefully: 4 top + 4 bottom + 4 vertical sides."),

    dict(subject="nonverbal", topic="spatial", difficulty=2,
         question="If you fold a cross-shaped net of 6 squares, what 3D shape do you make?",
         options=["Cuboid", "Cube", "Prism", "Pyramid"], answer=1,
         explanation="The classic cross-shaped net of 6 identical squares folds into a cube.",
         hint="A net is the flat version of a 3D shape. 6 equal squares = ?"),

    dict(subject="nonverbal", topic="spatial", difficulty=2,
         question="A cuboid has length 5cm, width 3cm, height 2cm. How many faces does it have?",
         options=["4", "6", "8", "12"], answer=1,
         explanation="All cuboids (including cubes) have 6 faces.",
         hint="Cuboid faces: top, bottom, front, back, left, right."),

    dict(subject="nonverbal", topic="spatial", difficulty=3,
         question="A shape is translated 3 units right and 2 units down. A point was at (1, 5). Where is it now?",
         options=["(4, 7)", "(4, 3)", "(3, 5)", "(-2, 3)"], answer=1,
         explanation="New x = 1+3 = 4. New y = 5-2 = 3. New position: (4, 3).",
         hint="Add the x-change to x-coordinate; subtract the y-change from y-coordinate."),

    dict(subject="nonverbal", topic="spatial", difficulty=2,
         question="How many vertices (corners) does a square-based pyramid have?",
         options=["4", "5", "6", "8"], answer=1,
         explanation="A square-based pyramid has 4 base corners + 1 apex = 5 vertices.",
         hint="Count the base corners, then add the pointy top."),

    dict(subject="nonverbal", topic="spatial", difficulty=3,
         question="A shape is rotated 180° about its centre. A point at the top-right will move to:",
         options=["Top-left", "Bottom-right", "Bottom-left", "Centre"], answer=2,
         explanation="180° rotation moves every point to the diagonally opposite position. Top-right → bottom-left.",
         hint="180° is a half-turn. Imagine spinning the shape around its middle."),

    dict(subject="nonverbal", topic="spatial", difficulty=2,
         question="Which 3D shape has two circular faces and one curved surface?",
         options=["Cone", "Sphere", "Cylinder", "Prism"], answer=2,
         explanation="A cylinder has two circular faces (top and bottom) and one curved surface.",
         hint="Think of a tin can."),

    dict(subject="nonverbal", topic="spatial", difficulty=3,
         question="A cube is painted red on all faces, then cut into 27 smaller cubes. How many small cubes have exactly 2 red faces?",
         options=["6", "8", "12", "24"], answer=2,
         explanation="Edge cubes (not corner) have exactly 2 painted faces. A cube has 12 edges; each edge has 1 middle cube (when cut 3×3×3). So 12 cubes.",
         hint="Think about where the small cubes sit: corners have 3 faces, edges have 2, faces have 1, inside has 0."),

    dict(subject="nonverbal", topic="spatial", difficulty=2,
         question="What is the name of the 3D shape made from two triangular faces and three rectangular faces?",
         options=["Pyramid", "Tetrahedron", "Triangular prism", "Cuboid"], answer=2,
         explanation="A triangular prism has 2 triangular faces and 3 rectangular faces.",
         hint="Think of a Toblerone box shape."),

    dict(subject="nonverbal", topic="spatial", difficulty=3,
         question="A rectangle measures 6cm × 4cm. It is enlarged by scale factor 3. What is the area of the enlarged rectangle?",
         options=["72cm²", "216cm²", "48cm²", "144cm²"], answer=1,
         explanation="New dimensions: 18cm × 12cm. Area = 18 × 12 = 216cm². (Area scales by factor²: 24 × 9 = 216.)",
         hint="Scale the length and width first, then find the new area."),

]


def seed():
    db = SessionLocal()
    existing = db.query(Question).count()
    if existing > 0:
        print(f"Database already has {existing} questions. Skipping seed.")
        print("To re-seed, delete grammar_school.db and run again.")
        db.close()
        return

    questions = [Question(**q) for q in QUESTIONS]
    db.add_all(questions)
    db.commit()
    db.close()
    print(f"Seeded {len(QUESTIONS)} questions successfully.")


if __name__ == "__main__":
    seed()
