from app import app, db, Plant, Treatment, BlogPost, Testimonial
from datetime import datetime, timedelta
import random

# Create application context
with app.app_context():
    # Drop existing tables and create new ones
    db.drop_all()
    db.create_all()
    
    # Sample plants
    plants = [
        {
            "name": "Ashwagandha",
            "scientific_name": "Withania somnifera",
            "description": "A powerful adaptogen that helps the body manage stress and promotes overall vitality.",
            "benefits": "Reduces stress and anxiety, improves sleep quality, boosts immunity, enhances energy levels, supports cognitive function, and promotes reproductive health in both men and women.",
            "usage": "Available as powder, capsules, or liquid extract. Typically taken daily (300-500mg twice daily) for stress management and overall wellbeing.",
            "image": "WhatsApp Image 2025-04-11 at 02.16.53_897faa01.jpg",
            "category": "herb",
            "conditions": "stress,immunity,energy,sleep,cognitive,reproductive"
        },
        {
            "name": "Turmeric",
            "scientific_name": "Curcuma longa",
            "description": "A powerful anti-inflammatory and antioxidant herb widely used in Ayurvedic medicine for centuries.",
            "benefits": "Reduces inflammation, supports joint health, improves digestion, enhances liver function, provides antioxidant protection, and supports cardiovascular health.",
            "usage": "Used in cooking, as supplements (400-600mg of curcumin three times daily), or as a paste for external application. The bioavailability increases when combined with black pepper.",
            "image": "turmeric.jpeg.jpg",
            "category": "root",
            "conditions": "inflammation,digestive,immunity,skin,joint"
        },
        {
            "name": "Tulsi (Holy Basil)",
            "scientific_name": "Ocimum sanctum",
            "description": "Revered as 'The Queen of Herbs' in Ayurveda for its numerous health benefits and sacred status in Hindu tradition.",
            "benefits": "Supports respiratory health, reduces stress and anxiety, boosts immunity, has antimicrobial properties, helps balance blood sugar, and supports cardiovascular health.",
            "usage": "Can be consumed as tea (2-3 cups daily), in cooking, or as supplements. Fresh leaves can be chewed daily for overall wellness.",
            "image": "WhatsApp Image 2025-04-11 at 02.15.59_1212c9e6.jpg",
            "category": "herb",
            "conditions": "stress,respiratory,immunity,skin,cardiovascular,diabetes"
        },
        {
            "name": "Brahmi",
            "scientific_name": "Bacopa monnieri",
            "description": "A nootropic herb that has been used in Ayurvedic medicine to enhance memory and cognitive function.",
            "benefits": "Improves memory and cognitive function, reduces anxiety and stress, has neuroprotective properties, and supports overall brain health.",
            "usage": "Available as powder, capsules, or liquid extract. Typically taken daily (300-450mg) for cognitive enhancement.",
            "image": "brahmi.jpg",
            "category": "herb",
            "conditions": "cognitive,memory,stress,neurological"
        },
        {
            "name": "Amla (Indian Gooseberry)",
            "scientific_name": "Phyllanthus emblica",
            "description": "One of the richest natural sources of Vitamin C and a powerful rejuvenating herb in Ayurveda.",
            "benefits": "Boosts immunity, improves digestion, enhances skin health, supports liver function, promotes healthy hair, and has strong antioxidant properties.",
            "usage": "Can be consumed fresh, as juice, powder, or in supplement form. Often included in triphala and chyawanprash formulations.",
            "image": "amla.jpg",
            "category": "fruit",
            "conditions": "immunity,digestive,skin,hair,liver"
        },
        {
            "name": "Shatavari",
            "scientific_name": "Asparagus racemosus",
            "description": "Known as the 'Queen of Herbs' in Ayurveda, particularly beneficial for women's health.",
            "benefits": "Supports female reproductive health, balances hormones, enhances lactation, improves digestive health, and has adaptogenic properties.",
            "usage": "Available as powder, capsules, or liquid extract. Typically taken daily (500mg twice daily) for hormonal balance and reproductive health.",
            "image": "shatavari.jpg",
            "category": "root",
            "conditions": "reproductive,hormonal,digestive,stress"
        }
    ]
    
    # Sample treatments
    treatments = [
        {
            "name": "Panchakarma",
            "description": "A comprehensive detoxification program that cleanses the body of toxins and restores balance to the doshas.",
            "benefits": "Eliminates toxins, improves digestion, enhances immunity, reduces stress, improves mental clarity, and promotes overall rejuvenation.",
            "procedure": "Involves five primary procedures: Vamana (therapeutic emesis), Virechana (purgation therapy), Basti (enema therapy), Nasya (nasal administration), and Raktamokshana (bloodletting therapy).",
            "image": "WhatsApp Image 2025-04-11 at 02.18.11_fb1bd5ec.jpg"
        },
        {
            "name": "Abhyanga",
            "description": "A therapeutic full-body massage with warm herbal oils tailored to your body constitution (dosha).",
            "benefits": "Nourishes tissues, improves circulation, reduces stress, promotes better sleep, enhances skin health, and removes toxins.",
            "procedure": "Warm herbal oil is applied to the entire body with specific massage techniques, followed by a warm bath or steam therapy.",
            "image": "WhatsApp Image 2025-04-11 at 02.17.22_474bc4c7.jpg"
        },
        {
            "name": "Shirodhara",
            "description": "A relaxing therapy that involves pouring a continuous stream of warm oil on the forehead, specifically on the 'third eye' area.",
            "benefits": "Calms the mind, improves focus, relieves anxiety, reduces headaches, improves sleep quality, and rejuvenates the nervous system.",
            "procedure": "The patient lies supine while warm herbal oil is poured in a steady stream on the forehead for 30-45 minutes, followed by a head massage.",
            "image": "WhatsApp Image 2025-04-11 at 02.18.59_1066c06c.jpg"
        },
        {
            "name": "Nasya",
            "description": "A nasal administration of herbal oils, powders, or pastes to cleanse the head and neck region.",
            "benefits": "Clears sinus congestion, improves respiratory function, enhances sensory perception, relieves headaches, and supports brain health.",
            "procedure": "After a brief facial massage, herbal oils or powders are administered through the nostrils in a controlled manner.",
            "image": "3-12.jpg"
        }
    ]
    
    # Sample blog posts
    blog_posts = [
        {
            "title": "The Power of Adaptogenic Herbs in Managing Modern Stress",
            "content": """
            In today's fast-paced world, stress has become an almost unavoidable part of daily life. While acute stress can be beneficial in certain situations, chronic stress can lead to a range of health issues, from weakened immunity to cardiovascular problems. This is where adaptogenic herbs come into play.
            ### What Are Adaptogens?
            Adaptogens are a unique group of herbal ingredients that help your body adapt to physical, chemical, and biological stress. They work by supporting the body's natural ability to counter adverse effects of stress and help restore normal physiological function.
            ### Key Adaptogenic Herbs in Ayurveda
            1. **Ashwagandha (Withania somnifera)**: Often called "Indian ginseng," ashwagandha helps reduce cortisol levels, improve sleep quality, and enhance overall vitality. Research suggests it can significantly reduce anxiety and stress levels.
            2. **Holy Basil (Tulsi)**: Beyond its spiritual significance, tulsi has powerful adaptogenic properties that help manage stress, support cognitive function, and boost immunity.
            3. **Brahmi (Bacopa monnieri)**: This herb not only helps the body adapt to stress but also enhances memory and cognitive function, making it particularly valuable in our mentally demanding world.
            4. **Shatavari (Asparagus racemosus)**: Especially beneficial for women, shatavari helps balance hormones while also providing adaptogenic benefits for managing stress.
            ### How to Incorporate Adaptogens Into Your Routine
            - **Herbal Teas**: A simple way to enjoy the benefits of adaptogens like tulsi and brahmi.
            - **Supplements**: Standardized extracts in capsule or tablet form provide consistent dosing.
            - **Powders**: Can be added to smoothies, oatmeal, or other foods.
            - **Ayurvedic Formulations**: Traditional preparations like Chyawanprash often contain multiple adaptogens.
            ### Precautions
            While adaptogens are generally safe, it's important to:
            - Consult with a healthcare provider before starting any new supplement.
            - Start with low doses and gradually increase.
            - Be patient – adaptogens typically work gradually over time, not overnight.
            """,
            "author": "Dr. Ayesha Verma",
            "date": datetime(2025, 4, 10)
        },
        {
            "title": "Why Ayurvedic Treatments Are Gaining Popularity Globally",
            "content": """
            Ayurveda, the ancient Indian system of medicine, is experiencing a global resurgence, as people look for natural and holistic ways to improve their health and well-being. Unlike conventional medicine, which often focuses on treating symptoms, Ayurveda seeks to address the root causes of illness by balancing the body, mind, and spirit.
            ### The Ayurvedic Approach to Health
            Ayurveda emphasizes the concept of balance. Health is considered a state of balance between the body's three primary energies, or doshas: Vata, Pitta, and Kapha. When these doshas are out of balance, disease occurs. Ayurvedic treatments aim to restore balance through diet, lifestyle modifications, herbal remedies, and specific therapies.
            ### Popular Ayurvedic Treatments
            - **Panchakarma**: A detoxification therapy that involves a series of treatments designed to eliminate toxins and restore balance.
            - **Abhyanga**: A rejuvenating full-body massage with warm herbal oils that nourish the body and improve circulation.
            - **Shirodhara**: A deeply relaxing therapy where warm oil is poured over the forehead to calm the mind and promote mental clarity.
            ### Why Choose Ayurveda?
            Many people are turning to Ayurveda because of its holistic approach. Unlike conventional medicine, Ayurveda looks at the person as a whole, considering physical, mental, and emotional well-being. It's also effective for managing chronic conditions and preventing disease before it starts.
            ### Conclusion
            Ayurvedic treatments are gaining popularity because they provide natural, holistic, and personalized solutions to health problems. Whether you're looking to improve your mental clarity, boost your immunity, or find relief from chronic pain, Ayurveda offers a wide range of remedies that can help restore your body and mind to their natural state of balance.
            """,
            "author": "Sita Rani",
            "date": datetime(2025, 4, 9)
        }
    ]
    
    # Add plants to the database
    for plant in plants:
        db.session.add(Plant(**plant))
    
    # Add treatments to the database
    for treatment in treatments:
        db.session.add(Treatment(**treatment))
    
    # Add blog posts to the database
    for post in blog_posts:
        db.session.add(BlogPost(**post))
    
    # Commit the session
    db.session.commit()
    
    print("Database seeded successfully.")
