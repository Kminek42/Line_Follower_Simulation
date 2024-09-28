# Line Follower Simulation

I created this simulation to train a recursive neural network controlling a line-following robot.
All elements in this simulation operate as vector operations, allowing the use of optimizations from the numpy library.

## How to run

Before you start:

run `pip3 install -r requirements.txt` command in terminal to instll all necessary libraries.

## Track
The `track.py` file generates the track procedurally. One can run `python3 track.py` to see different results. The Track class has a `distance_to_chain` method that returns the distance between any point and the track.
<img height="512" alt="Screenshot 2024-04-03 at 08 26 29" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/93e219be-d0eb-406a-ac07-843c5c2c9349">

## Robot
The `robot.py` file simulates a robot with two wheels. The Robot class is initialized with the length and wheelbase as a numpy array, allowing testing of many different variants simultaneously. In this presentation, the robot dimensions are constant, and the algorithm only determines the neural network weights. One can use the move(motor_l, motor_r) method to set the target speed, which will be achieved with a specified acceleration to simulate the robot's inertia. The robot also has a `get_sensors` method that returns readings from all sensors (using distance to the track).
<img height="512" alt="image" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/3d6bfc1f-6124-4bef-a8f9-f33819c7a48e">

## Learning
Learning is done using a genetic algorithm that adjusts the neural network weights. The quality indicator of the genotype is the average speed at which the robot moved along the track. Turning around, turning at intersections, or leaving the track results in setting the average speed to 0. The mutation rate gradually increases when the next generation is worse than the previous one. After training using the train.py file, One can see progress by running `python3 plot_evolution.py BestScore.csv AverageScore.csv MutationRate.csv`.
<img height="512" alt="image" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/4c1fbda4-f3f7-4cdd-88cb-a1372a1b7cf4">

An example of learning outcome. Despite preserving two individuals from the previous generation, sometimes the result of the next generation worsens. This is due to the added noise to the readings, which introduces some randomness into the simulation.<br><br>
The `learn.py` file also creates a `genotype.txt` file, which can be pasted into the `main.py` file.
One can run the `main.py` file to see the simulation with the trained NN model.<br>

<img height="512" alt="image" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/612dc692-0f61-4360-840d-1d556e0dab3d">
