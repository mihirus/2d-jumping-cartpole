import casadi as cas
import numpy as np

class Manipulator:
  @staticmethod
  def generate_M(T, q_dot):
    return(cas.jacobian(cas.gradient(T, q_dot), q_dot))

  @staticmethod
  def generate_C(M, q, q_dot):
    q_dim = q.shape[0]
    Jm = cas.jacobian(M, q)
    C = cas.reshape(Jm @ q_dot, q_dim, q_dim)

    for i in range(q_dim):
      C_part = -0.5 * Jm.T[:, q_dim*i : q_dim*(i+1)] @ q_dot
      C[:, i] += C_part

    return C
  
  @staticmethod
  def generate_G(V, q):
    return(cas.gradient(V, q))