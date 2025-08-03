# OpenEPI x UNLEASH Hackathon (Team 11 - Sustainable Farming Advisor)

## Team Members
- Dominic Mills-Howell (Team Lead)
- Shubham Singh
- Safita Ardhia 
- Priyanshu

# Installation Steps

## Builiding and Running the Flask App with Nix 
The most straightforward way to build and run this application is by installing [Nix](https://nixos.org/download/#nix-install-linux) and cloning this repository then running the following commands inside a terminal within this repo

```
nix-shell
flask run
```

Nothing more is needed and you can view the app running at `localhost:5000`. Under the hood, Nix is a creating an ephemeral shell that that downloads and configures the environment defined in the `default.nix` file of this reposistory. All of these actions take place on disk so it provides a convinenet way of creating an isolated environmenet that doesn't interact/pollute your global system. 

## Builiding and Running the Flask App without Nix 
Enter the following commands to get the application up and running if you choose to not use.

```
export FLASK_APP=app.py  
export FLASK_ENV=development

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
flask run
```

# Written Product Description
## What problem are you solving?

As climate change accelerates, communities around the world are seeking practical, local solutions to mitigate its effects. One promising approach is the use of sustainable farming, which refers to using agricultural methods that meet today’s food needs without compromising the ability of future generations to do the same.

An example of sustainable farming is a technique like polyculture planting, such as growing complementary crops such as corn, beans, and squash together, enhance biodiversity, soil health, and resilience. Yet while the theory is simple, implementation is not. Transitioning to sustainable farming is complex, requiring localised knowledge (that respect local traditions especially), access to specific materials, and adaptation to unpredictable constraints.

A major challenge is the lack of a supportive, accessible platform where individuals can log their progress, share successes, ask questions, and learn from others in similar conditions. For example, someone in one region might easily acquire a material like PVC piping for a hydroponics project, while someone elsewhere must improvise with limited resources, and may not even know what alternatives suitable exist or can be used. This is the main problem we're solving: tackling the lack of an centralised means for developing and sharing accessible, locally-adapted sustainable farming solutions. 



## What is your solution?

A platform that empowers users to plan, document, troubleshoot, and share their  sustainable farming efforts. It serves as both a guide and a community which highlights successful case studies, providing context-sensitive advice, and helping users navigate setbacks, especially when working under constrained conditions.

We propose a web application, written in [Flask](https://flask.palletsprojects.com/en/stable/), that determines the most suitable sustainable farming method for a user to use, from inputting their location data and available land area for farming. It works in the following three step process:

### **Step 1: Get a Recommended Farming Method**

Users begin on the **home screen**, which is split into two main sections:

* The **top half** displays an interactive global map with clickable regions.
* The **bottom half** contains two input fields:

  * On the **left**, the user enters the **country** where they plan to start their sustainable farming project.
  * On the **right**, they input the **amount of land area** (e.g., in square meters or acres) available for farming.

Once both fields are filled out, the user clicks the **“Recommend Farming Method”** button. Two key things then happen:

1. **Contextual Insights from the Community**
   If other users have previously implemented sustainable farming projects under similar conditions (e.g., same region or land size), the system:

   * Draws **animated dashed lines** on the map pointing to their locations.
   * Displays a **pop-up over each relevant project site**, prompting the user to explore how others solved similar challenges.

2. **Personalized Farming Method Recommendation**
   Below the button, the system displays:

   * A recommended sustainable farming method (e.g., **Aquaponics**, **Agroforestry**, or **Vertical Farming**).
   * A clickable link labeled **“Let’s get you started,”** which leads the user to the **Field Notes** section, where they begin planning and documenting their project (covered in Step 2).

> **How the Recommendation Works**
> Behind the scenes, the system uses the user's location to query OpenEPI’s [Soil API](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#soil) and [Weather API](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#weather).
> It converts the user’s coordinates and land area into a **bounding box**, retrieves:

* The **dominant soil type**
* Current **weather data** (e.g., temperature, rainfall)

These inputs along with the land size are passed into a rules-based algorithm that suggests the most appropriate farming method as shown in the table below.

| Method            | Climate Benefit                          |
| ----------------- | ---------------------------------------- |
| Aeroponics        | Minimal water use                        |
| Agroforestry      | Carbon capture, soil and water retention |
| Regenerative Agriculture   | Soil health, carbon sequestration        |
| Aquaponics        | Closed-loop sustainability               |
| Vertical Farming  | Urban, low-land use, weather-proof       |
| Dryland Farming   | Thrives in arid conditions               |
| Silvopasture      | Climate-smart livestock integration      |
| Greenhouses  | Control over climate variables           |

If either soil or weather data is unavailable, the algorithm falls back to using land area alone to provide a best-effort recommendation.

* **Step 2**: Create and Track Your Project (Field Notes)

   * After clicking “Let’s get you started,” users are taken to the Field Notes section—where they begin documenting their sustainable farming journey.

    * At the top of the page is a brief getting started guide tailored to the recommended farming method. This guide outlines basic steps, materials needed (adapted to local constraints), and links to relevant resources.

    * Below that is a text box where users can log updates about their project at different stages—for example, planning, setup, planting, troubleshooting, or harvesting.

    * Users can also upload images of their crops and receive feedback on crop health using OpenEPI’s [Crop Health](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#crop-health) API, which provides automated assessments based on visual indicators.

    * Each post can be tagged with the type of crops being grown and any specific local or traditional farming methods used. This improves discoverability and makes it easier for others to learn from contextually similar projects.

* **Step 3**: Join the Community (Community Notes)

    * Once a user creates their first post, it becomes visible in the Community Notes section:
        * Other users can comment, ask questions, or offer suggestions—fostering collaboration and collective problem-solving.
        * The tagging system enables users to search for similar projects based on crop type, location, method, or materials used.
        * This creates a living network of shared experiences—making it easier to replicate or adapt successful sustainable farming efforts across diverse regions and conditions.



## Further refinements/Future implementations

## Who are your users and what is their impact?
Our users are individuals and communities who are motivated to implement sustainable farming practices, but face barriers due to limited resources, local constraints, or lack of tailored guidance. They generally fall into the following groups:

1. **Small-scale farmers and gardeners**
   These users are looking to grow food for themselves or their communities, often on small plots of land. They want practical, low-cost solutions adapted to their local climate and available materials. Many are eager to experiment with techniques like permaculture, agroforestry, or aquaponics but lack access to expert guidance.

2. **Educators, students, and youth programs**
   Sustainability and food systems are increasingly central in school curricula and community outreach programs. Our platform offers a hands-on, interactive way for young people and educators to document and reflect on real-world farming experiments—tying together science, climate education, and civic engagement.

3. **Urban dwellers and homesteaders**
   In cities and towns, people interested in self-sufficiency or community gardening often have access to very limited land. They need highly space-efficient methods like vertical farming or container gardening, and our platform helps them explore what’s feasible for their context.

4. **Development workers and NGOs**
   Organizations working in areas affected by food insecurity or climate vulnerability need adaptable, replicable methods for growing food locally. The ability to learn from case studies in similar regions and document their own implementations makes our platform valuable for both field operations and long-term planning.

5. **Tinkerers, DIYers, and open-source advocates**
   Some users are drawn not just to farming but to the engineering and community problem-solving aspects—those interested in hacking together hydroponics systems or designing resource-efficient greenhouses with locally available materials. These users contribute to the knowledge base and help others adapt solutions to their context.

## What is your business plan?

Our goal is to build a sustainable, community-driven platform that grows through user contribution, strategic partnerships, and open access to data and tools. The business plan focuses on three key areas: growth, sustainability, and long-term impact.

### 1. **Launch and Growth Strategy**

We will begin by targeting early adopters, such as community garden groups, permaculture forums, educators, and local farming co-ops, who are already experimenting with sustainable methods but lack a platform to document, troubleshoot, and share their work. These users are highly motivated and likely to contribute high-quality content and feedback.

We’ll also:

* Partner with NGOs, schools, and university programs involved in environmental science or agriculture to seed early field note content.
* Integrate multilingual and low-bandwidth accessibility features to reach underserved communities.
* Create open challenges (e.g., “build a low-cost aquaponics system using only local materials”) to drive engagement and experimentation.

### 2. **Revenue Model**

Our platform is free to use for individuals. Revenue and sustainability will be achieved through:

* **Institutional Licensing**: Organizations (e.g., development agencies, universities, local governments) can license private versions of the platform with analytics dashboards, training materials, and integration with their internal systems.
* **Donor and Grant Funding**: We will actively seek funding through climate resilience, food security, and open knowledge grants—such as those offered by FAO, the Green Climate Fund, and Mozilla.
* **Marketplace (Future Phase)**: In the long term, we may host a vetted, peer-rated marketplace of materials, kits, and services (e.g., seed exchanges, recycled irrigation systems, tool libraries) where local vendors can connect with growers.
* **Premium Support or Custom Deployments**: For organizations seeking tailored deployments (e.g., in refugee camps, remote villages), we will offer consulting and technical services.

### 3. **Community and Knowledge Network**

User-contributed data (e.g., crop growth patterns, material availability, local adaptation strategies) becomes part of a growing, open-access repository. Over time, this will form a living library of context-specific sustainable farming practices, helping drive research, policy, and localized development.

Our long-term goal is to be the GitHub + Wikipedia for grassroots farming: a participatory platform where anyone, anywhere, can learn, contribute, and adapt sustainable practices that work in their real-world context.

---


## Who is the team that is going to deliver in this?




