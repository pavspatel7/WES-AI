# from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

# Predefined list of questions and answers
qa_pairs = [

    # Greetings
    ("What is your name?", "I'm a chatbot created by WesAI."),
    ("Hi", "Hello! How can I assist you with your Rutgers University questions today?"),
    ("Good morning", "Good morning! I hope you have a great day ahead. What Rutgers-related information can I provide for you?"),
    ("Good evening", "Good evening! What can I help you find or do related to Rutgers University tonight?"),
    

    # Locations
    ("What is the address of the Rutgers University main campus?", "Rutgers University's main campus address is 7 College Ave, New Brunswick, NJ 08901."),

    # Busch
    ("Where is Busch Student Center BSC located address", "604 Bartholomew rd Piscataway, NJ 08854"),

    # Livi
    ("Where is Liviston Student Center LSC located address", "84 joyce Kilmer ave, Piscataway, NJ 08854"),
    ("Where is the Rutgers Business School located?", "Rutgers Business School is located at 100 Rockafeller Rd, Piscataway, NJ 08854 on the Livingston Campus."),
    ("I m at College Avenue / clg ave Campus, How to go to Rutgers Business School / RBS on Livingston Campus?", "To get to the Rutgers Business School on the Livingston Campus from the College Avenue Campus, the LX bus is the most direct route, providing a straightforward connection between these two points."),
    ("I m at College Avenue / clg ave Campus, how to get to livingston / livi", "You can take Bus LX which goes to Livingston"),
    ("I m at busch student center, how to get to livingston ", "You can take either Bus B or B/BE which goes to Livingston"),
    ("I m at busch student center, how to get to livi ", "You can take either Bus B or B/BE which goes to Livingston"),
    
    # Cook
    ("Where can I find the Douglass Student Center?", "The Douglass Student Center is located at 100 George St, New Brunswick, NJ 08901."),
    

    ("Where is the Rutgers Athletic Center (RAC) located?", "The Rutgers Athletic Center, or RAC, is located at 83 Rockafeller Rd, Piscataway, NJ 08854 on the Livingston Campus."),
    ("Where is the Rutgers Student Activities Center (SAC) located?", "The Rutgers Student Activities Center (SAC) is located at 613 George St, New Brunswick, NJ 08901."),
    
    

    # Advising
    ("How can I contact Rutgers University admissions?", "Rutgers University admissions can be contacted via phone at (732) 445-4636 or email at admissions@rutgers.edu."),
    ("How to apply for financial aid at Rutgers?", "To apply for financial aid at Rutgers, students must complete the Free Application for Federal Student Aid (FAFSA) annually. Rutgers' federal school code is 002629. Additionally, students should check their Rutgers status on the Financial Aid portal for any additional documents required and for scholarship opportunities."),
    ("Can I switch my parking permit if I change my living situation or campus affiliation?", "If your living situation or campus affiliation changes, you may be eligible to switch your parking permit. Contact Rutgers Department of Transportation Services directly to request a change based on your new circumstances."),

    # Information
    ("Rutgers University library system..", "The Rutgers University library system includes multiple libraries, such as Alexander Library on College Ave Campus, Carr Library on Livingston Campus, and the Douglass Library on Douglass Campus."),
    ("How to access Rutgers WebReg?", "Rutgers WebReg can be accessed online through the Rutgers portal or directly at webreg.rutgers.edu. A NetID and password are required for login."),
    ("How to get a parking permit at Rutgers University?", "Parking permits at Rutgers University can be obtained through the Rutgers Department of Transportation Services website or at their office at 55 Commercial Ave, New Brunswick, NJ 08901."),
    ("What is the procedure for Rutgers course registration?", "Rutgers course registration is done through WebReg. Students need their Rutgers NetID and password to log in and can select courses based on their eligibility and availability."),
    ("How to find employment opportunities at Rutgers University?", "Employment opportunities at Rutgers University can be found on the Rutgers University Human Resources website under the 'Jobs at Rutgers' section."),
    ("What clubs and organizations are available at Rutgers?", "Rutgers University hosts over 700 student clubs and organizations. A full list and details can be found on the Rutgers Involvement website."),
    ("Where to get Rutgers University merchandise?", "Rutgers University merchandise can be purchased at the Rutgers University Barnes & Noble Bookstore located at 100 Somerset St, New Brunswick, NJ 08901 or https://rutgers.bncollege.com."),
    ("What is the best way to travel between Rutgers campuses?", "The best way to travel between Rutgers campuses in New Brunswick/Piscataway is by using the Rutgers Campus Bus System. The service is free for students, faculty, and staff. There are several bus routes connecting the different campuses including the College Avenue, Busch, Livingston, and Cook/Douglass campuses."),
    ("What are the housing options at Rutgers?", "Rutgers University offers a range of housing options including traditional dorms, apartments, and living-learning communities. Housing is available on all New Brunswick/Piscataway campuses. Students can apply for housing through the Residence Life website, where they can also find information about rates and amenities."),
    ("What are the requirements for graduation at Rutgers?", "Graduation requirements at Rutgers vary by school and major but generally include completing a minimum number of credits, fulfilling major and core curriculum requirements, and maintaining a minimum GPA. Students should consult their academic advisor and their school's website for specific requirements."),

    #Library
    ("What are the library hours at Rutgers University?", "The library hours at Rutgers University vary by location and time of year. Generally, during the semester, the Alexander Library is open 24 hours from Sunday 10 am until Friday at 10 pm, and Saturday hours are 10 am to 6 pm. Check the Rutgers Libraries website for specific hours of other libraries and for changes during holidays and exam periods."),
    

    # Dining
    ("What are the dining options at Rutgers University?", "Rutgers University offers various dining options across its campuses, including Brower Commons on College Ave Campus and the Livingston Dining Commons on Livingston Campus."),
    ("What dining options are available at Rutgers?", "Rutgers University offers a variety of dining options across its campuses, including dining halls, cafes, and food courts. Meal plans are available for students. Each campus has its own dining services, with options ranging from traditional dining halls to international cuisines and fast-food chains."),
    

    # Health
    ("Where is the Rutgers Health Services located?", "Rutgers Health Services has multiple locations, including the Hurtado Health Center at 11 Bishop Place, New Brunswick, NJ 08901."),
    ("How can I access mental health services at Rutgers?", "Mental health services at Rutgers are provided through the Counseling, ADAP, and Psychiatric Services (CAPS). Students can access free and confidential counseling, crisis intervention, and psychiatric services by contacting CAPS or visiting their offices on campus. Telehealth options are also available."),
    ("How to get involved in research at Rutgers?", "Students interested in research opportunities can start by talking to their professors, exploring department websites, and checking the Undergraduate Research portal. Rutgers offers various programs and grants for undergraduates to engage in research, including Aresty Research Assistant Program."),
    

    # Buses
    ("What are the Rutgers bus routes?", "Rutgers University's bus system includes several routes connecting the different campuses: A (College Ave to Busch), B (Busch to Livingston), C (College Ave to Livingston), EE (College Ave to Cook/Douglass), F (College Ave to Cook/Douglass via George St), LX (Livingston to College Ave), and REXB (Cook/Douglass to Busch)."),
    ("What bus route should I take to reach the Rutgers Student Center from the Livingston Campus?", "To reach the Rutgers Student Center from the Livingston Campus, you can take the LX bus. This bus route will take you directly to the College Avenue Campus, where the Rutgers Student Center is located."),
    ("Is there a bus that goes directly between Busch and Livingston Campuses?", "Yes, the B bus provides a direct route between the Busch and Livingston Campuses without stopping at other campuses."),
    ("Which Rutgers bus goes to the Livingston Campus?", "The LX and B buses provide service to the Livingston Campus. The LX bus connects the Livingston Campus with the College Avenue Campus, while the B bus connects Livingston to the Busch Campus."),
    ("How do I get to the College Avenue Campus from Busch Campus?", "To travel from the Busch Campus to the College Avenue Campus, you can take the A, H, or LX buses. The A and H buses offer direct routes, while the LX bus provides a more roundabout route but still connects these campuses."),
    ("What bus should I take to get to the Cook/Douglass Campus?", "The F, EE, and REXB buses serve the Cook/Douglass Campus. The F bus connects the College Avenue Campus to Cook/Douglass directly. The EE bus provides a route that connects the College Avenue Campus, downtown New Brunswick, and then the Cook/Douglass Campus. The REXB bus connects the Busch Campus directly to Cook/Douglass."),
    ("What bus connects to the Rutgers Health Services on the Cook/Douglass Campus?", "The F and EE buses provide routes to the Cook/Douglass Campus, where Rutgers Health Services is located. You can catch these buses from the College Avenue Campus."),
    ("Which bus goes to Livingston Campus?", "The B route and LX route buses go to Livingston Campus. B route connects Busch Campus with Livingston, and LX route connects Livingston Campus with College Avenue Campus."),
    ("Where does the A bus stop?", "The A bus stops include the College Avenue Student Center on College Ave Campus and the Busch Student Center on Busch Campus, among others. It's a direct route between College Avenue and Busch campuses."),
    ("How do I get from College Avenue Campus to Cook/Douglass Campus?", "To get from College Avenue Campus to Cook/Douglass Campus, you can take the EE or F bus. The EE bus route includes stops like the College Avenue Student Center and the Red Oak Lane on Douglass Campus. The F route also connects these campuses but takes a different path through George Street."),


    ("How does Rutgers support international students?", "Rutgers supports international students through the Center for Global Services, which offers advising on immigration, cultural adjustment, and academic issues. The center also organizes programs and events to help international students integrate into the university community."),
    

    
    
    
    
    
    ("What bus should I take from the Rutgers Student Center to the Werblin Recreation Center?", "From the Rutgers Student Center on College Avenue Campus, you should take the A bus to reach the Werblin Recreation Center on Busch Campus."),
    
    ("Which bus stop is closest to the Rutgers Cinema on Livingston Campus?", "The closest bus stop to the Rutgers Cinema on Livingston Campus is the Livingston Plaza or the Livingston Student Center. The LX and B buses have stops at both locations, making them convenient for reaching the cinema."),
    
    ("What's the nearest bus stop to the Rutgers Athletic Center (RAC) on Livingston Campus?", "The nearest bus stop to the Rutgers Athletic Center (RAC) on Livingston Campus is the Yellow Lot stop. You can take the LX or B route to get there."),
    ("What types of parking permits are available at Rutgers?", "Rutgers University offers several types of parking permits: Student permits for residential and commuter students, Faculty/Staff permits, and Visitor permits. Specific permits are designated for each campus - College Avenue, Busch, Livingston, and Cook/Douglass."),
    ("How can I purchase a parking permit at Rutgers?", "Parking permits at Rutgers can be purchased online through the Rutgers Department of Transportation Services website. Students, faculty, and staff need to log in with their NetID to access the permit application and payment system."),
    ("Where can I park with a commuter permit on the College Avenue Campus?", "With a College Avenue commuter permit, you can park in designated commuter lots on the College Avenue Campus, such as Lot 26, Lot 30, and the College Avenue Deck. Always check the current parking map for any updates or changes."),
    ("Can I use my Livingston residential permit to park on other campuses?", "A Livingston residential permit primarily allows parking on the Livingston Campus in designated residential lots. However, there may be specific lots on other campuses where overnight parking is permitted. Check the Rutgers Transportation Services website for the most current cross-campus parking rules."),
    ("What are the rules for parking on campus during a snow emergency?", "During a snow emergency, parking rules on campus may change to facilitate plowing and safe passage. Typically, this may require moving your vehicle to specific lots or garages. Always check the Rutgers Department of Transportation Services website or your Rutgers email for official instructions during these events."),
    ("Are there any restrictions on where I can park overnight?", "Overnight parking is restricted to certain lots and is generally reserved for residential permit holders. Commuter students are typically not allowed to park overnight. Specific lots that permit overnight parking can be found on the Transportation Services website."),
    ("How do visitors park at Rutgers?", "Visitors to Rutgers can park in designated visitor lots or use metered parking available across the campuses. It's recommended to purchase a visitor parking pass from the Department of Transportation Services website for extended visits, which details the permissible parking locations."),
    ("What happens if I park in the wrong lot at Rutgers?", "Parking in the wrong lot or without a proper permit may result in a citation or your vehicle being towed. It's important to always park according to the regulations of your specific permit and to check for any temporary changes in parking rules."),
    

    ("Tell me a joke", "Why don't some couples go to the gym? Because some relationships don't work out! 😄 But at Rutgers, we believe in working out and strong partnerships. How can I assist you further?"),
    ("Make me laugh", "Did you hear about the mathematician who's afraid of negative numbers? He will stop at nothing to avoid them! As for us, we're not afraid of tough questions. What's on your mind about Rutgers?"),
    ("Where is Busch Student Center BSC located address", "604 Bartholomew rd Piscataway, NJ 08854"),
    ("I m at livingston student center, how to get Busch", "You can take either Bus B or B/BE which goes to Busch"),
    ("Where is Liviston Student Center LSC located address", "84 joyce Kilmer ave, Piscataway, NJ 08854"),
    
    ("Which stop should i get out at livi? i want to go to yellow lot", "You can stop at livinston plaza which is near to yellow lot"),
    ("What is the address of the Rutgers University main campus?", "Rutgers University's main campus address is 7 College Ave, New Brunswick, NJ 08901."),
    ("Where is the Rutgers Business School located?", "Rutgers Business School is located at 100 Rockafeller Rd, Piscataway, NJ 08854 on the Livingston Campus."),
    ("How can I contact Rutgers University admissions?", "Rutgers University admissions can be contacted via phone at (732) 445-4636 or email at admissions@rutgers.edu."),
    ("Where can I find the Douglass Student Center?", "The Douglass Student Center is located at 100 George St, New Brunswick, NJ 08901."),
    ("What is the Rutgers University library system?", "The Rutgers University library system includes multiple libraries, such as Alexander Library on College Ave Campus, Carr Library on Livingston Campus, and the Douglass Library on Douglass Campus."),
    ("How to go at Carr Dickson Library at Livi?", "You can stop at livinston student center if taking bus or address is 75 Avenue E, Piscataway, NJ 08854"),
    ("From livi/livingston, How to go at Library at Busch?", "You can take the B or B/He bus from the Livingston Student Center to the Busch Student Center. Both the B and B/He buses stop at the Busch Student Center, which is close to the Library of Science and Medicine (Library at Busch). You can get off at the Busch Student Center stop and walk to the library."),
    ("address of busch library or library of science and medicine?" , "165 Bevier Road Piscataway, NJ 08854 United States"),
    ("How can I contact the office of financial-aid", "you can visit https://scarlethub.rutgers.edu/financial-services/office-of-financial-aid/ ,call 234-433-5356 or email financialoffice@rutgers.edu"),
    ("How to access Rutgers WebReg?", "Rutgers WebReg can be accessed online through the Rutgers portal or directly at webreg.rutgers.edu. A NetID and password are required for login."),
    ("Where is the Rutgers Health Services located?", "Rutgers Health Services has multiple locations, including the Hurtado Health Center at 11 Bishop Place, New Brunswick, NJ 08901."),
    ("what some food places restaurants on near livingston campus plaza student center", "there is sabaro pizza, starbucks, Dunkin donuts, kilmer market, qdoba and Henery's diner located on livinston campus"),
    ("what some food places restaurants on near Busch campus student center", "there is Moe's southwest grill, Panera, Gerald's pizzaria and Starbucks truck located near Busch Student Center"),
    ("where can I Register for parking permit can I park parking registration", "you can Buy parking permit for you vehicle at https://rudots.nupark.com/v2/Portal/Login?ReturnUrl=%2Fv2%2Fportal "), 


    ("What are the dining options at Rutgers University?", "Rutgers University offers various dining options across its campuses, including Brower Commons on College Ave Campus and the Livingston Dining Commons on Livingston Campus."),
    ("How to get a parking permit at Rutgers University?", "Parking permits at Rutgers University can be obtained through the Rutgers Department of Transportation Services website or at their office at 55 Commercial Ave, New Brunswick, NJ 08901."),
    ("Where is the Rutgers Athletic Center (RAC) located?", "The Rutgers Athletic Center, or RAC, is located at 83 Rockafeller Rd, Piscataway, NJ 08854 on the Livingston Campus."),
    ("What is the procedure for Rutgers course registration?", "Rutgers course registration is done through WebReg. Students need their Rutgers NetID and password to log in and can select courses based on their eligibility and availability."),
    ("How to find employment opportunities at Rutgers University?", "Employment opportunities at Rutgers University can be found on the Rutgers University Human Resources website under the 'Jobs at Rutgers' section."),
    ("Where is the Rutgers Student Activities Center (SAC) located?", "The Rutgers Student Activities Center (SAC) is located at 613 George St, New Brunswick, NJ 08901."),
    ("What clubs and organizations are available at Rutgers?", "Rutgers University hosts over 700 student clubs and organizations. A full list and details can be found on the Rutgers Involvement website."),
    ("Where to get Rutgers University merchandise?", "Rutgers University merchandise can be purchased at the Rutgers University Barnes & Noble Bookstore located at 100 Somerset St, New Brunswick, NJ 08901 or online."),
    ("What are the library hours at Rutgers University?", "The library hours at Rutgers University vary by location and time of year. Generally, during the semester, the Alexander Library is open 24 hours from Sunday 10 am until Friday at 10 pm, and Saturday hours are 10 am to 6 pm. Check the Rutgers Libraries website for specific hours of other libraries and for changes during holidays and exam periods."),
    ("How to apply for financial aid at Rutgers?", "To apply for financial aid at Rutgers, students must complete the Free Application for Federal Student Aid (FAFSA) annually. Rutgers' federal school code is 002629. Additionally, students should check their Rutgers status on the Financial Aid portal for any additional documents required and for scholarship opportunities."),
    ("What is the best way to travel between Rutgers campuses?", "The best way to travel between Rutgers campuses in New Brunswick/Piscataway is by using the Rutgers Campus Bus System. The service is free for students, faculty, and staff. There are several bus routes connecting the different campuses including the College Avenue, Busch, Livingston, and Cook/Douglass campuses."),
    ("What dining options are available at Rutgers?", "Rutgers University offers a variety of dining options across its campuses, including dining halls, cafes, and food courts. Meal plans are available for students. Each campus has its own dining services, with options ranging from traditional dining halls to international cuisines and fast-food chains."),
    ("How can I access mental health services at Rutgers?", "Mental health services at Rutgers are provided through the Counseling, ADAP, and Psychiatric Services (CAPS). Students can access free and confidential counseling, crisis intervention, and psychiatric services by contacting CAPS or visiting their offices on campus. Telehealth options are also available."),
    ("What are the housing options at Rutgers?", "Rutgers University offers a range of housing options including traditional dorms, apartments, and living-learning communities. Housing is available on all New Brunswick/Piscataway campuses. Students can apply for housing through the Residence Life website, where they can also find information about rates and amenities."),
    ("How to get involved in research at Rutgers?", "Students interested in research opportunities can start by talking to their professors, exploring department websites, and checking the Undergraduate Research portal. Rutgers offers various programs and grants for undergraduates to engage in research, including Aresty Research Assistant Program."),
    ("What are the requirements for graduation at Rutgers?", "Graduation requirements at Rutgers vary by school and major but generally include completing a minimum number of credits, fulfilling major and core curriculum requirements, and maintaining a minimum GPA. Students should consult their academic advisor and their school's website for specific requirements."),
    ("How does Rutgers support international students?", "Rutgers supports international students through the Center for Global Services, which offers advising on immigration, cultural adjustment, and academic issues. The center also organizes programs and events to help international students integrate into the university community."),
    ("Which Rutgers bus goes to the Livingston Campus?", "The LX and B buses provide service to the Livingston Campus. The LX bus connects the Livingston Campus with the College Avenue Campus, while the B bus connects Livingston to the Busch Campus."),
    ("How do I get to the College Avenue Campus from Busch Campus?", "To travel from the Busch Campus to the College Avenue Campus, you can take the A, H, or LX buses. The A and H buses offer direct routes, while the LX bus provides a more roundabout route but still connects these campuses."),
    ("What bus should I take to get to the Cook/Douglass Campus?", "The F, EE, and REXB buses serve the Cook/Douglass Campus. The F bus connects the College Avenue Campus to Cook/Douglass directly. The EE bus provides a route that connects the College Avenue Campus, downtown New Brunswick, and then the Cook/Douglass Campus. The REXB bus connects the Busch Campus directly to Cook/Douglass."),
    ("Is there a bus that goes directly between Busch and Livingston Campuses?", "Yes, the B bus provides a direct route between the Busch and Livingston Campuses without stopping at other campuses."),
    ("What bus route should I take to reach the Rutgers Student Center from the Livingston Campus?", "To reach the Rutgers Student Center from the Livingston Campus, you can take the LX bus. This bus route will take you directly to the College Avenue Campus, where the Rutgers Student Center is located."),
    ("How can I get from the College Avenue Campus to the Rutgers Business School on Livingston Campus?", "To get to the Rutgers Business School on the Livingston Campus from the College Avenue Campus, the LX bus is the most direct route, providing a straightforward connection between these two points."),
    ("What bus connects to the Rutgers Health Services on the Cook/Douglass Campus?", "The F and EE buses provide routes to the Cook/Douglass Campus, where Rutgers Health Services is located. You can catch these buses from the College Avenue Campus."),
    ("Which bus route is best for getting to the Werblin Recreation Center on Busch Campus?", "The A and H buses provide the most direct routes to the Werblin Recreation Center on the Busch Campus. These buses can be caught from the College Avenue Campus and other points on the Busch Campus."),
    ("If I need to travel between all four campuses, which bus route is most efficient?", "The most efficient way to travel between all four Rutgers campuses (College Avenue, Busch, Livingston, and Cook/Douglass) is to use a combination of the LX, A/H, and F/EE buses. Planning your trip based on the specific campuses you need to visit and the time of day is advisable for the most efficient route."),
    ("What are the Rutgers bus routes?", "Rutgers University's bus system includes several routes connecting the different campuses: A (College Ave to Busch), B (Busch to Livingston), C (College Ave to Livingston), EE (College Ave to Cook/Douglass), F (College Ave to Cook/Douglass via George St), LX (Livingston to College Ave), and REXB (Cook/Douglass to Busch)."),
    ("Which bus goes to Livingston Campus?", "The B route and LX route buses go to Livingston Campus. B route connects Busch Campus with Livingston, and LX route connects Livingston Campus with College Avenue Campus."),
    ("Where does the A bus stop?", "The A bus stops include the College Avenue Student Center on College Ave Campus and the Busch Student Center on Busch Campus, among others. It's a direct route between College Avenue and Busch campuses."),
    ("How do I get from College Avenue Campus to Cook/Douglass Campus?", "To get from College Avenue Campus to Cook/Douglass Campus, you can take the EE or F bus. The EE bus route includes stops like the College Avenue Student Center and the Red Oak Lane on Douglass Campus. The F route also connects these campuses but takes a different path through George Street."),
    ("What bus should I take from the Rutgers Student Center to the Werblin Recreation Center?", "From the Rutgers Student Center on College Avenue Campus, you should take the A bus to reach the Werblin Recreation Center on Busch Campus."),
    ("How to travel from Livingston Campus to the Rutgers Business School?", "To travel from Livingston Campus to the Rutgers Business School located on the Livingston Campus, you can simply use the LX bus route which connects the Livingston Plaza with the Livingston Student Center, or walk as both are located within the same campus."),
    ("Which bus stop is closest to the Rutgers Cinema on Livingston Campus?", "The closest bus stop to the Rutgers Cinema on Livingston Campus is the Livingston Plaza or the Livingston Student Center. The LX and B buses have stops at both locations, making them convenient for reaching the cinema."),
    ("What's the nearest bus stop to the Rutgers Athletic Center (RAC) on Livingston Campus?", "The nearest bus stop to the Rutgers Athletic Center (RAC) on Livingston Campus is the Yellow Lot stop. You can take the LX or B route to get there."),
    ("What types of parking permits are available at Rutgers?", "Rutgers University offers several types of parking permits: Student permits for residential and commuter students, Faculty/Staff permits, and Visitor permits. Specific permits are designated for each campus - College Avenue, Busch, Livingston, and Cook/Douglass."),
    ("How can I purchase a parking permit at Rutgers?", "Parking permits at Rutgers can be purchased online through the Rutgers Department of Transportation Services website. Students, faculty, and staff need to log in with their NetID to access the permit application and payment system."),
    ("Where can I park with a commuter permit on the College Avenue Campus?", "With a College Avenue commuter permit, you can park in designated commuter lots on the College Avenue Campus, such as Lot 26, Lot 30, and the College Avenue Deck. Always check the current parking map for any updates or changes."),
    ("Can I use my Livingston residential permit to park on other campuses?", "A Livingston residential permit primarily allows parking on the Livingston Campus in designated residential lots. However, there may be specific lots on other campuses where overnight parking is permitted. Check the Rutgers Transportation Services website for the most current cross-campus parking rules."),
    ("What are the rules for parking on campus during a snow emergency?", "During a snow emergency, parking rules on campus may change to facilitate plowing and safe passage. Typically, this may require moving your vehicle to specific lots or garages. Always check the Rutgers Department of Transportation Services website or your Rutgers email for official instructions during these events."),
    ("Are there any restrictions on where I can park overnight?", "Overnight parking is restricted to certain lots and is generally reserved for residential permit holders. Commuter students are typically not allowed to park overnight. Specific lots that permit overnight parking can be found on the Transportation Services website."),
    ("How do visitors park at Rutgers?", "Visitors to Rutgers can park in designated visitor lots or use metered parking available across the campuses. It's recommended to purchase a visitor parking pass from the Department of Transportation Services website for extended visits, which details the permissible parking locations."),
    ("What happens if I park in the wrong lot at Rutgers?", "Parking in the wrong lot or without a proper permit may result in a citation or your vehicle being towed. It's important to always park according to the regulations of your specific permit and to check for any temporary changes in parking rules."),
    ("Can I switch my parking permit if I change my living situation or campus affiliation?", "If your living situation or campus affiliation changes, you may be eligible to switch your parking permit. Contact Rutgers Department of Transportation Services directly to request a change based on your new circumstances."),
    
    ("Tell me a joke", "Why don't some couples go to the gym? Because some relationships don't work out! 😄 But at Rutgers, we believe in working out and strong partnerships. How can I assist you further?"),
    ("Make me laugh", "Did you hear about the mathematician who's afraid of negative numbers? He will stop at nothing to avoid them! As for us, we're not afraid of tough questions. What's on your mind about Rutgers?"),
    
    ("How can I make a chatbot?", "You can use various NLP libraries and frameworks."),
    ("What courses does Dr. Emily Johnson teach?", "Dr. Emily Johnson teaches Mathematics and Statistics."),
    ("Is the Algorithms course taught by Dr. Imelenski open?", "No, the Algorithms course taught by Dr. Imelenski is currently closed."),
    ("Who teaches the Genetics course?", "The Genetics course is taught by Dr. Rodriguez and Prof. Martinez."),
    ("Are there any open sections for the Database Systems course?", "Yes, there is an open section taught by Prof. Johnson."),
    ("Which professor teaches Cell Biology?", "Cell Biology is taught by Dr. Brown and Prof. Davis."),
    ("Is there a closed section for the Cognitive Psychology course?", "Yes, there is a closed section for the Cognitive Psychology course."),
    ("Who teaches the Abnormal Psychology course?", "The Abnormal Psychology course is taught by Dr. Martinez and Prof. Johnson."),
    ("What courses are available under the Biology major?", "Under the Biology major, you can take courses such as Cell Biology, Genetics, and Ecology."),
    ("Is there an open section for the Algorithms course?", "Yes, there is an open section for the Algorithms course taught by Dr. Cowen."),
    ("Where can I register for a parking permit?", "You can register for a parking permit for your vehicle at https://rudots.nupark.com/v2/Portal/Login?ReturnUrl=%2Fv2%2Fportal."),




]

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings for the questions for faster retrieval
question_embeddings = np.array(model.encode([q for q, _ in qa_pairs]))


def home(request):
    return render(request, 'index.html')


@csrf_exempt  # Disable CSRF temporarily for simplicity
def ask(request):
    if request.method == 'POST':
        user_question = json.loads(request.body).get('question', '')

        # Encode the user question to get the embedding
        user_question_embedding = model.encode(user_question)

        # Compute semantic similarity
        similarities = util.pytorch_cos_sim(user_question_embedding, question_embeddings)

        # Find the index of the highest similarity score
        most_similar_idx = np.argmax(similarities)

        # Fetch the corresponding answer
        _, answer = qa_pairs[most_similar_idx]

        return JsonResponse({"question": user_question, "answer": answer})

    return JsonResponse({"error": "Request must be POST"}, status=400)
