# OpenEPI x UNLEASH Hackathon (Team 11 - Sustainable Farming Advisor)

## Team Members
- Dominic Mills-Howell (Team Lead)
- Shubham Singh
- Safita Ardhia 
- Priyanshu Tomar

# Installation Steps

This web application is built with Flask. You can run it using either **Nix** (recommended) or a standard Python environment.

## Option 1: Build and Run with Nix (Recommended)

The simplest and cleanest way to run the app is using [Nix](https://nixos.org/download/#nix-install-linux), which sets up a fully isolated environment based on the configuration in this repo.

### Steps:

1. **Install Nix** (if not already installed):
    [nixos.org/download](https://nixos.org/download/#nix-install-linux)

2. **Clone this repository** and open a terminal in the project directory.

3. **Start the app** by running:

   ```bash
   nix-shell
   flask run
   ```

The app will be available at **`http://localhost:5000`**.

> Behind the scenes, `nix-shell` creates a **temporary shell environment** using the `default.nix` file. This ensures all dependencies are installed without modifying your global system, making it ideal for reproducible development.

## Option 2: Build and Run Without Nix (Using Python Virtual Environment)

If you'd rather run the app using a traditional Python setup, follow these steps:

### Steps:

1. **Set the Flask environment variables**:

   ```bash
   export FLASK_APP=app.py  
   export FLASK_ENV=development
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the app**:

   ```bash
   flask run
   ```

Once again, you can access the app at **`http://localhost:5000`**.


# Written Product Description
## What problem are you solving?

As climate change accelerates, communities around the world are seeking practical, local solutions to mitigate its effects. One promising approach is the use of sustainable farming, which refers to using agricultural methods that meet today’s food needs without compromising the ability of future generations to do the same.

An example of sustainable farming is a technique like polyculture planting, where growing complementary crops such as corn, beans, and squash together, enhance biodiversity, soil health, and resilience. Yet while the theory is simple, the implementation is not. Transitioning to sustainable farming is complex, requiring localised knowledge (that are sensitive to the needs of local traditions), access to specific materials, and adaptation to unpredictable constraints.

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

2. **Personalised Farming Method Recommendation**
   Below the button, the system displays:

   * A recommended sustainable farming method (e.g., **Aquaponics**, **Agroforestry**, or **Vertical Farming**).
   * A clickable link labeled **“Let’s get you started,”** which leads the user to the **Field Notes** section, where they begin planning and documenting their project (covered in Step 2).

> **How the Recommendation Works**
> Behind the scenes, the system uses the user's location to query OpenEPI’s [Soil API](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#soil) and [Weather API](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#weather).
> It converts the user’s coordinates and land area into a **bounding box**, retrieves:

* The **dominant soil type**
* Current **weather data** (e.g., temperature, rainfall)

These inputs along with the land size are passed into a rules-based algorithm that suggests the most appropriate farming method as shown in the table below.

<div align="center">

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

</div>

If either soil or weather data is unavailable, the algorithm falls back to using land area alone to provide a best-effort recommendation.

### **Step 2: Create and Track Your Project (Field Notes)**

* After clicking “Let’s get you started,” users are taken to the Field Notes section, where they can begin documenting their sustainable farming journey.

* At the top of the page is a brief getting started guide tailored to the recommended farming method. This guide outlines basic steps, materials needed (adapted to local constraints), and links to relevant resources.

* Below that is a text box where users can log updates about their project at different stages, for example, planning, setup, planting, troubleshooting, or harvesting.

* Users can also upload images of their crops and receive feedback on crop health using OpenEPI’s [Crop Health](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#crop-health) API, which provides automated assessments based on visual indicators.

* Each post can be tagged with the type of crops being grown and any specific local or traditional farming methods used. This improves discoverability and makes it easier for others to learn from contextually similar projects.

### **Step 3: Join the Community (Community Notes)**

* Once a user creates their first post, it becomes visible in the Community Notes section:
    * Other users can comment, ask questions, or offer suggestions—fostering collaboration and collective problem-solving.
    * The tagging system enables users to search for similar projects based on crop type, location, method, or materials used.
    * This creates a living network of shared experiences—making it easier to replicate or adapt successful sustainable farming efforts across diverse regions and conditions.



## Further refinements/Future implementations

As we continue development, we intend to refine several elements of the existing application. Below are some of the areas identified for improvement (this list is not exhaustive):

* Creating a more robust algorithm for determining the best suited sustainable farming method from a given set of constraints. The current heuristics used are broad and lack the appropriate level of rigour and precision to adequately determine the whether the conditions correspond to the most suitable sustainable farming method for the widest possible ranges of possible scenarios. Some ways to better refine would be to reify the methods from this [paper](https://www.atmosp.physics.utoronto.ca/people/lev/ESSgc2/farmEIAeval.pdf), such as environmental risk mappings, life cycle analysis and multi-agent systems, to name a few. Worth noting are the arguments presented in [this paper](https://link.springer.com/content/pdf/10.1007/s13593-015-0305-2.pdf) as well. These can be used either individually or a combination of the methods depending on our specific objective(s).
* Increase the range of crops and their associated diesease that can be verified and diagnised with the Crop Health API with pattern matching and machine learning models. The current crop health API is limited by a number of crops, for instance, the multi-HLT prediction only has predictions for five types of crops namely: cassava, maize, beans, bananas and cocoa. As the number of users on this platform increases, it opens up the possiblity for labeling and diagnosing the crop health for a much larger variety of crops.
* Enhancing the user interface (UI) to be more intuitive and user-centric. While the current UI is functional, certain elements may come across as generic or lacking in distinctive identity. Our goal is to redesign key interface components to improve usability, reduce cognitive load, and provide a more engaging and memorable user experience. This includes re-evaluating layout hierarchies, visual feedback mechanisms, and interaction flows based on user behavior and feedback.


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
   Some users are drawn not just to farming but to the engineering and community problem-solving aspects, like those interested in hacking together hydroponics systems or designing resource-efficient greenhouses with locally available materials (including some of our group members). These users contribute to the knowledge base and help others adapt solutions to their context.

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
* **Marketplace (Future Phase)**: In the long term, we may host a vetted, peer-rated marketplace of materials, kits, and services (e.g., seed exchanges, recycled irrigation systems, tool libraries) where local vendors can connect with growers.
* **Premium Support or Custom Deployments**: For organizations seeking tailored deployments (e.g., in refugee camps, remote villages), we will offer consulting and technical services.

### 3. **Community and Knowledge Network**

User-contributed data (e.g., crop growth patterns, material availability, local adaptation strategies) becomes part of a growing, open-access repository. Over time, this will form a living library of context-specific sustainable farming practices, helping drive research, policy, and localized development.

Our long-term goal is to be the GitHub + Wikipedia for grassroots farming: a participatory platform where anyone, anywhere, can learn, contribute, and adapt sustainable practices that work in their real-world context.

## Who is the team that is going to deliver in this?

Our team is a diverse and multidisciplinary group of innovators, each bringing unique strengths in technology, governance, and implementation.

**Dominic Mills-Howell** is the team lead, a research scientist turned software engineer originally from Jamaica and now based in the UAE. With a background in full-stack development, DevOps, infrastructure, and tooling, Dominic combines strong technical breadth with deep problem-solving skills. He holds bachelor’s and master’s degrees in mathematics from the University of the West Indies and a postgraduate diploma from the International Centre for Theoretical Physics in Italy. A former researcher at CERN and current lead for the OpenEPIxUNLEASH Hackathon team, he brings both scientific rigor and practical experience in building scalable systems.

**Shubham M. Singh** is an electronics and communication engineer currently working at [Redicine Medsol](https://www.redicinemedsol.com/), an Indian health-tech startup. There, he plays a key role in developing the country’s first patented IoT-based Smart Pillbox, supporting public health infrastructure through real-time medication tracking and digital health worker tools. His technical expertise is complemented by experience in operations and inventory management, ensuring end-to-end project delivery at scale.

**Priyanshu Tomar** is pursuing a degree in Computer Science and Artificial Intelligence at Newton School of Technology, Rishihood University. As an emerging technologist, he brings fresh energy and up-to-date knowledge of AI, modern development practices, and product experimentation to the team.

**Safita Ardhia** is a co-founder of [Voices4Budget](https://voices4budget.org/en) and an advocate for environmental sustainability, transparency, and inclusive governance. With expertise in civic technology and anti-corruption initiatives, she contributes a global perspective on policy engagement and user-centric digital solutions. Her participation in programs like [HackCorruption](https://hackcorruption.org/) has equipped her with insight into how technology can be applied ethically and equitably for societal benefit.

Together, our team blends technical excellence, operational reliability, user-centered thinking, and a commitment to social impact. This combination allows us to build not just functional tools, but meaningful solutions that address real-world problems in a sustainable way.


