### Variational Autoencoder for both Classification and Regression of Autocorrelated Data

This is the implementation of the Classifying VAE and Classifying VAE+LSTM models, as described in [_A Classifying Variational Autoencoder with Application to Polyphonic Music Generation_](https://arxiv.org/abs/1711.07050) by Jay A. Hennig, Akash Umakantha, and Ryan C. Williamson.

[Exowanderer](github.com/exowanderer) extended the Classifying-VAE to a Classifying-and-Regressing-VAE (i.e. a `VAEPredictor`)
[PhilippeSaade11](github.com/philippesaade11) created the genetic algorithm to optimize the hyperparameters

These models extend the standard VAE and VAE+LSTM to the case where there is a latent category associated with regression or classification. 

### Original Case
In the case of music generation, for example, we may wish to infer the key of a song (i.e. class), so that we can generate notes that are consistent with that key. These discrete latents are modeled as a Logistic Normal distribution, so that random samples from this distribution can use the reparameterization trick during training.

The training data contained in this repo includes the JSB Chorales and Piano-midi corpuses can be found in `data/input`. Songs have been transposed into C major or C minor (`*_Cs.pickle`), for comparison to previous work, or kept in their original keys (`*_all.pickle`).

### DeepSkyes Case
In case of simulating 1D exoplanet spectra, we want to use simulated spectra to build a VAE that can generate new spectra with given physical parameters (i.e. T_planet, M_planet, R_planet, C/O, [Fe/H], Cloud+Haze).  We use public exoplanet spectral databases and retreival algorithms to generated highly augmented features for the VAE and planetary properties.

We use the [ExoTransmit-PLATON](https://github.com/exowanderer/platon), [CHIMERA](https://github.com/ExoCTK/exoctk), and [Goyal-Exeter](https://bd-server.astro.ex.ac.uk/exoplanets/) public codes/databases to simulate exoplanet spectrum for both training and validation.

### VAE-Predictor

[Exowanderer](github.com/exowanderer) restructored the [Classify-VAE](https://github.com/mobeets/classifying-vae-lstm) routines to input any 1D data sets, and for any size of VAE-Prediction topology, for both classification and regression.

### Genetic Algorithm
[PhilippeSaade11](github.com/philippesaade11) created a genetic algorithm that inputs the VAEPredictor class into a Chromosome class to optimize the hyperparameters.

### Current Stage

We are currently experimenting and testing the genetic algorithm to improve on the MNIST hand-written digit classification scheme. This is almost complete (March 29 2019), and we will soon move onto training for regression with the exoplanet spectral databases.
