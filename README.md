# Drone-Route-Planning

This project aims to develop a UAV route planning software to cover large areas efficiently. The use cases involve having multiple drones at hand, and also have multiple charging locations for the drones, which significantly increase the complexity of the problem.

## Table Of Contents

  * [Setup instructions](#setup-instructions)
  * [Plots](#plots)
  * [Contributors](#contributors)


## Setup instructions

1. Clone the repository on your system.

2. Navigate to the project directory, then
    - For Linux, make setup.sh executable, then run it.
   
          * `chmod +x setup.sh`

          *  `./setup.sh`
    - For Windows, run the bat file as is in the cmd.
    
          * `setup.bat`

3. To run any program in this project, always use the virtual environment -
    - For Linux, run `source venv/bin/activate` 
    - For Windows, run `venv\Scripts\activate.bat`

4. Run vrp.py to see the plots with the calculated paths. 

> Note: All plots are tested on maharashtra shapefile.

## Plots
![Clustering plots](https://raw.githubusercontent.com/theViz343/drone-route-planning/master/plots/clusterplot.jpg) 
![Route Plot](https://raw.githubusercontent.com/theViz343/drone-route-planning/master/plots/vrpplot.jpg)

> Try to play with the parameters to get different results

## Contributors

[Vishwesh Pillai](https://github.com/theViz343)

[Yash mantri](https://github.com/yashm1)
