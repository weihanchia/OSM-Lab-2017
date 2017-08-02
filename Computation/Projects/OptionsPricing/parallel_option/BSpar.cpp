/* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 *
 * This file contains routines to serially compute the call and
 * put price of an European option.
 *
 * Simon Scheidegger -- 06/17.
 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#include <algorithm>    // Needed for the "max" function
#include <cmath>
#include <iostream>
#include <omp.h>


/* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 A simple implementation of the Box-Muller algorithm, used to
generate gaussian random numbers; necessary for the Monte Carlo
method below. */

double gaussian_box_muller(unsigned int seed) {
  double x = 0.0;
  double y = 0.0;
  double euclid_sq = 0.0;

  // Continue generating two uniform random variables
  // until the square of their "euclidean distance"
  // is less than unity
  do {
    x = 2.0 * rand_r(&seed) / static_cast<double>(RAND_MAX)-1;
    y = 2.0 * rand_r(&seed) / static_cast<double>(RAND_MAX)-1;
    euclid_sq = x*x + y*y;
  } while (euclid_sq >= 1.0);

  return x*sqrt(-2*log(euclid_sq)/euclid_sq);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla call option with a Monte Carlo method

double monte_carlo_call_price(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T) {
  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;
  unsigned int seed = 1;

  for (int i=0; i<num_sims; i++) {
    seed += 1;
    double gauss_bm = gaussian_box_muller(seed);
    S_cur = S_adjust * exp(sqrt(v*v*T)*gauss_bm);
    payoff_sum += std::max(S_cur - K, 0.0);
  }

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla call option with a Monte Carlo method Parallel

double monte_carlo_call_price_p(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T) {
  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;
  unsigned int seed;

  #pragma omp parallel shared(S_adjust, payoff_sum) private(S_cur, seed)
  {
    seed = omp_get_thread_num();
    #pragma omp for reduction (+:payoff_sum)
    for (int i=0; i<num_sims; i++) {
      seed += omp_get_max_threads();
      double gauss_bm = gaussian_box_muller(seed);
      S_cur = S_adjust * exp(sqrt(v*v*T)*gauss_bm);
      payoff_sum += std::max(S_cur - K, 0.0);
    }
  }

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}
// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla put option with a Monte Carlo method

double monte_carlo_put_price(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T) {
  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;
  unsigned int seed = 1;

  for (int i=0; i<num_sims; i++) {
    seed += 1;
    double gauss_bm = gaussian_box_muller(seed);
    S_cur = S_adjust * exp(sqrt(v*v*T)*gauss_bm);
    payoff_sum += std::max(K - S_cur, 0.0);
  }

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla put option with a Monte Carlo method Parallel

double monte_carlo_put_price_p(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T) {
  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;
  unsigned int seed;

  #pragma omp parallel shared(S_adjust, payoff_sum) private(S_cur, seed)
  {
    seed = omp_get_thread_num();
    #pragma omp for reduction (+:payoff_sum)
    for (int i=0; i<num_sims; i++) {
      seed += omp_get_max_threads();
      double gauss_bm = gaussian_box_muller(seed);
      S_cur = S_adjust * exp(sqrt(v*v*T)*gauss_bm);
      payoff_sum += std::max(K - S_cur, 0.0);
    }
  }

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

int main(int argc, char **argv) {

  // Parameters
  int num_sims = 10000000;   // Number of simulated asset paths
  double S = 100.0;  // Option price
  double K = 100.0;  // Strike price
  double r = 0.05;   // Risk-free rate (5%)
  double v = 0.2;    // Volatility of the underlying (20%)
  double T = 1.0;    // One year until expiry

  // Then we calculate the call/put values via Monte Carlo
  double time_p = -omp_get_wtime();
  double call_p = monte_carlo_call_price_p(num_sims, S, K, r, v, T);
  double put_p = monte_carlo_put_price_p(num_sims, S, K, r, v, T);
  time_p += omp_get_wtime();

  double time = -omp_get_wtime();
  double call = monte_carlo_call_price(num_sims, S, K, r, v, T);
  double put = monte_carlo_put_price(num_sims, S, K, r, v, T);
  time += omp_get_wtime();

  // Finally we output the parameters and prices
  std::cout << "Number of Paths: " << num_sims << std::endl;
  std::cout << "Underlying:      " << S << std::endl;
  std::cout << "Strike:          " << K << std::endl;
  std::cout << "Risk-Free Rate:  " << r << std::endl;
  std::cout << "Volatility:      " << v << std::endl;
  std::cout << "Maturity:        " << T << std::endl;

  std::cout << "Call Price (P):  " << call_p << std::endl;
  std::cout << "Call Price (S):  " << call << std::endl;
  std::cout << "Put Price (P):   " << put_p << std::endl;
  std::cout << "Put Price (S):   " << put << std::endl;
  std::cout << "P Time:      " << time_p << std::endl;
  std::cout << "S Time:      " << time << std::endl;

  return 0;
}
