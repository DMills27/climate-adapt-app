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
   
* Step 1: 
    * The upper half of the home screen presents a global map with clickable components. The bottom half of the screen from the left-hand side has a text box where the user enters the country that they are planning on undertaking the sustainable farming activity for then the amount of available area of land they have available for farming on the right
    * After entering those details and clicking the 'Recommend Farming Method' two things should happen: 
        1) If one or more users has already implemented a project with similar constraints, it notifies the user of that by drawing an animated dashed line or lines to their location where that user implemented that solution and then a pop-up over their location appears prompting the user to view it; 
        2) The recommended sustainable farming method appears under the button and under that is a clickable hyperlink with text that says "Let's get you started". Clicking that will take you to the page where you'll document your progress detailed further in the section below.
        * **Note**: The algorithm recommends a sustainable farming method by using the user's location to retrieve soil type and weather data via OpenEPI's [Soil API](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#soil) and  [Weather API](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#weather). It converts the given coordinates and land area into a bounding box, then queries the APIs to get the dominant soil type and current weather (e.g., temperature, rainfall). These inputs, along with land size, are evaluated using simple heuristics to determine the best method, such as Aquaponics, Agroforestry, or Vertical Farming, as shown in the table below. If soil or weather data is missing, the algorithm defaults to using land area alone.
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

* Step 2: 
    * After clicking the "Let's get you started" link, you enter the "field notes" section of the application. The top of the page contains a preamble about how to get started with the farming method that was recommended, and the type of materials that would be available to needed to actualise this project. Under that is a text box where one can create posts about the varous progress of your project in different time intervals. In addition to creating posts one can upload images of the crops and get feedback on the health of the crops at various stages which uses the OpenEPI [Crop Health](https://github.com/openearthplatforminitiative/openepi-client-py?tab=readme-ov-file#crop-health) API under the hood.
    * The upper 
* Step 3:


## Further refinements/Future implementations

## Who are your users and what is their impact?
Our general demographic are people interesting in cultivating small to medium size farming projects as well as established farmers interested in boosting their farming businesses by offering training and knowledge sharing sessions.  

## What is your business plan?

## Who is the team that is going to deliver in this?




