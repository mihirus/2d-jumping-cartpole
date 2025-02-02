import casadi as cas
import numpy as np

# Create lists that will contain all objects
def get_data_structures():
  variable_upper_bounds = []
  variable_lower_bounds = []
  variable_initial_conditions = []
  constraints = []
  constraint_lower_bounds = []
  constraint_upper_bounds = []
  
  return variable_lower_bounds, variable_upper_bounds, variable_initial_conditions, constraints, constraint_lower_bounds, constraint_upper_bounds

# All of the below assume (timestep, state, input) as the order in all variable lists
# Can be used to populate variable bounds and initial conditions
def populate_list_properties(list, state_variable_property, input_variable_property, timestep_property, N):
  list.append(timestep_property)
  
  for i in range(N):
    list.append(state_variable_property)
  
  for i in range(N):
    list.append(input_variable_property)

# Assume that there is always exactly one timestep variable
# Allow for lower and upper bound so that you can leave something free
def set_boundary_conditions(lower_bounds_list, upper_bounds_list, lower_bound, upper_bound, pos):
  lower_bounds_list[1 + pos] = lower_bound
  upper_bounds_list[1 + pos] = upper_bound

# for when it has already been converted to an array
def set_boundary_conditions_array(lower_bounds_array, upper_bounds_array, lower_bound, upper_bound, pos):
  lower_bounds_array[1 + pos : 1 + pos + lower_bound.shape[0]] = lower_bound
  upper_bounds_array[1 + pos : 1 + pos + upper_bound.shape[0]] = upper_bound

# To set initial conditions to a trajectory
def set_initial_conditions_array(array, initial_conditions, pos):
  # array[1 + pos : 1 + pos + initial_conditions.shape[0]] = initial_conditions[:]
  initial_conditions[1 : 1 + array.shape[0]] = np.hstack(array)

def populate_variables_and_constraints(x_dim, u_dim, constraints_list, constraint_lower_bounds, constraint_upper_bounds, f, N):
  state_variables_list = []
  input_variables_list = []
  
  h = cas.SX.sym('h')
  state_variables_list.append(h)
  
  for i in range(N):
      x_i = cas.SX.sym('x' + str(i), x_dim)
      u_i = cas.SX.sym('u' + str(i), u_dim)
      state_variables_list.append(x_i)
      input_variables_list.append(u_i)
      
      if i > 0:
        ## APPROACH 1: SEPARATE VARIABLE FOR HALF POINT
        # x_i_half = cas.MX.sym('x_half' + str(i), 4) # halfway between i and i-1
        # w.append(x_i_half)
        # g.append(x_i_half - 0.5*(x_i + x_i_last) - 0.125*h*(f(x_i_last, u_i_last)+f(x_i, u_i)))
        # g.append(x_i - x_i_last - (h/6)*(f(x_i, u_i) + 4*f(x_i_half, 0.5*(u_i_last + u_i)) + f(x_i_last, u_i_last)))
        
        ## APPROACH 2: COMPRESSED FORM, NO EXTRA VARIABLE
        constraints_list.append(x_i - x_i_last - (h/6)*(f(x_i, u_i) + 4*f(0.5*(x_i + x_i_last) + 0.125*h*(f(x_i_last, u_i_last)+f(x_i, u_i)), 0.5*(u_i_last + u_i)) + f(x_i_last, u_i_last)))
        
        constraint_lower_bounds.append(np.zeros((x_dim)))
        constraint_upper_bounds.append(np.zeros((x_dim)))
      
      x_i_last = x_i
      u_i_last = u_i
  
  return state_variables_list, input_variables_list # this is so you can formulate a cost function elsewhere

# indexed so you can connect together multiple loops
def populate_variables_and_constraints_indexed(x_dim, u_dim, constraints_list, constraint_lower_bounds, constraint_upper_bounds, f, N, index):
  state_variables_list = []
  input_variables_list = []

  h = cas.SX.sym('h_phase' + str(index))
  state_variables_list.append(h)

  for i in range(N):
      x_i = cas.SX.sym('x_phase' + str(index) + '_' + str(i), x_dim)
      u_i = cas.SX.sym('u_phase' + str(index) + '_' + str(i), u_dim)
      state_variables_list.append(x_i)
      input_variables_list.append(u_i)

      if i > 0:
        ## APPROACH 1: SEPARATE VARIABLE FOR HALF POINT
        # x_i_half = cas.MX.sym('x_half' + str(i), 4) # halfway between i and i-1
        # w.append(x_i_half)
        # g.append(x_i_half - 0.5*(x_i + x_i_last) - 0.125*h*(f(x_i_last, u_i_last)+f(x_i, u_i)))
        # g.append(x_i - x_i_last - (h/6)*(f(x_i, u_i) + 4*f(x_i_half, 0.5*(u_i_last + u_i)) + f(x_i_last, u_i_last)))

        ## APPROACH 2: COMPRESSED FORM, NO EXTRA VARIABLE
        constraints_list.append(x_i - x_i_last - (h/6)*(f(x_i, u_i) + 4*f(0.5*(x_i + x_i_last) + 0.125*h*(f(x_i_last, u_i_last)+f(x_i, u_i)), 0.5*(u_i_last + u_i)) + f(x_i_last, u_i_last)))

        constraint_lower_bounds.append(np.zeros((x_dim)))
        constraint_upper_bounds.append(np.zeros((x_dim)))

      x_i_last = x_i
      u_i_last = u_i

  return state_variables_list, input_variables_list # this is so you can formulate a cost function elsewhere

def extract_variable_array(output, starting_position, period, N):
  res = []
  for i in range(N):
    res.append(output[starting_position + i*period])
  
  return np.array(res)
  