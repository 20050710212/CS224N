#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(X, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    the backward propagation for the gradients for all parameters.

    Notice the gradients computed here are different from the gradients in
    the assignment sheet: they are w.r.t. weights, not inputs.

    Arguments:
    X -- M x Dx matrix, where each row is a training example x.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = np.reshape(params[ofs:ofs+ Dx * H], (Dx, H))
    ofs += Dx * H
    b1 = np.reshape(params[ofs:ofs + H], (1, H))
    ofs += H
    W2 = np.reshape(params[ofs:ofs + H * Dy], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:ofs + Dy], (1, Dy))

    # Note: compute cost based on `sum` not `mean`.
    ### YOUR CODE HERE: forward propagation
    z1 = np.dot(X, W1) + b1    #(M * Dx)(Dx * H) = M * H
    h = sigmoid(z1)
    z2 = np.dot(h, W2) + b2
    y_hat = softmax(z2)
    cost = -np.sum(labels * np.log(y_hat))/ np.shape(X)[0] # the result is from M examples, 
    ### END YOUR CODE

    ### YOUR CODE HERE: backward propagation
    M = np.shape(X)[0]
    dz2 = y_hat - labels       #(M * Dy)
    dW2 = np.dot(h.T, dz2) / M #(H * M)(M * Dy) = H * Dy, although M is diminished, the result is actually caused by M examples,so need a mean operation
    db2 = np.mean(dz2,axis=0, keepdims=True)  # dz2 has M*Dy b2 is 1 * Dy, need a mean operation 
    
    dh  = np.dot(dz2, W2.T)    #(M * Dy)(Dy * H) = M * H
    dz1 = dh*sigmoid_grad(h)   #(M * H)(M * H) = M * H# I havenoidea why it is h
    dW1 = np.dot(X.T,dz1)/ M   #(Dx * M)(M * H) = Dx * H, a mean operation is in need.
    db1 = np.mean(dz1,axis=0, keepdims=True)           #
    
    gradW2 = dW2
    gradb2 = db2
    gradW1 = dW1
    gradb1 = db1
    ### END YOUR CODE
#     ### YOUR CODE HERE: forward propagation
#    h = sigmoid(np.dot(X,W1) + b1)
#    yhat = softmax(np.dot(h,W2) + b2)
#    ### END YOUR CODE
#    ### YOUR CODE HERE: backward propagation
#    cost = np.sum(-np.log(yhat[labels==1])) / X.shape[0]
#    d3 = (yhat - labels) / X.shape[0]
#    gradW2 = np.dot(h.T, d3)
#    gradb2 = np.sum(d3,0,keepdims=True)
#    dh = np.dot(d3,W2.T)
#    grad_h = sigmoid_grad(h) * dh
#    gradW1 = np.dot(X.T,grad_h)
#    gradb1 = np.sum(grad_h,0)
#    ### END YOUR CODE

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    return cost, grad


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print "Running sanity check..."

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in xrange(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print "Running your sanity checks..."
    ### YOUR CODE HERE
    #raise NotImplementedError
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
