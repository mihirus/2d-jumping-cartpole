Run all in jupyter notebook to create dynamics model, optimize over it, apply controls to simulation, and plot resulting trajectories.

Currently only ground phase before jump works, optimizing over jump dynamics has not been accomplished. This is because the jump dynamics (to convert from ground state vector to rigid body angular and linear momentum) involve a square root, and CasADi is unhappy. However, it is trivial to constrain the jump to be purely vertically oriented.

File description:
- 2d-jumping-cartpole.xml: MJCF formatted XML used to define MuJoCo systems
- dynamics_model.py: Static methods to generate manipulator matrices M, C, G given casadi expressions T, V, q, q_dot
- trajopt_setup.py: Utility functions to generate trajectory optimization data structures
- [X]to[Y]interpolated.csv: CSV files containing pre-generated state and input plans, can be loaded to avoid having to re-optimize

![](./from_x-1_ydot0.5_pannedview_cropped.gif)