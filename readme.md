<h1>Line Follower Simulation</h1>

I have created this simulation to train recurrent neural network that controls the line follower.
All elements in this simulation work as vectorized operations, to they can utilize numpy's optimization.

<h2>Track</h2>
track.py generates the track procedurally. Run 'python3 track.py' to see different results. Track object has 'distance_to_chain' method which return distance between any point and track.


<img height="512" alt="Screenshot 2024-04-03 at 08 26 29" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/93e219be-d0eb-406a-ac07-843c5c2c9349">

<h2>Robot</h2>
robot.py simulates differential wheeled robot. Robot class is initialized with length and wheelbase as numpy's array which allows to test many different variations at once. One can use move(motor_l, motor_r) method to set target velocity, which will be changed with certain acceleration, in order to simulate robot's inertia. Robot also has 'get_sensors' method which returns reading from all sensors (using distance to track).

Robot is controlled by RobotController class. It has neural network with 2 memory cells which allows to memorize where the line was.

<img height="512" alt="image" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/3d6bfc1f-6124-4bef-a8f9-f33819c7a48e">

<h2>Learning</h2>
Learning is implemented by a genetic algorithm that adjusts the weights of the neural network. Mutation rate is increasing gradually when the next generation is worse than previous. After training using train.py one can see progress by running 'python3 plot_evolution.py BestScore.csv MutationRate.csv'. 

<img height="512" alt="image" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/fbfd79ea-df19-4ab1-b328-bfa68316b78c">

Example of learning result.

learn.py also creates genotype.txt file which can be pasted into main.py file.


Run main.py file to see the simulation with trained NN.

<img height="512" alt="image" src="https://github.com/Kminek42/Line_Follower_Simulation/assets/51884463/669ee7f7-1a69-4d30-a10b-328897254e98">
