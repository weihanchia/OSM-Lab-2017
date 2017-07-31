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
#include <vector>

using namespace std;


/* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 A simple implementation of the Box-Muller algorithm, used to
generate gaussian random numbers; necessary for the Monte Carlo
method below. */

double gaussian_box_muller() {
  double x = 0.0;
  double y = 0.0;
  double euclid_sq = 0.0;

  // Continue generating two uniform random variables
  // until the square of their "euclidean distance"
  // is less than unity
  do {
    x = 2.0 * rand() / static_cast<double>(RAND_MAX)-1;
    y = 2.0 * rand() / static_cast<double>(RAND_MAX)-1;
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

  for (int i=0; i<num_sims; i++) {
    double gauss_bm = gaussian_box_muller();
    S_cur = S_adjust * exp(sqrt(v*v*T)*gauss_bm);
    payoff_sum += std::max(S_cur - K, 0.0);
  }

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing an Asian vanilla call option with a Monte Carlo method

double monte_carlo_call_price_asian(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T, const int& t, const vector <double>& tvec) {
  double S_adjust = S * exp(tvec[0]*(r-0.5*v*v));
  double payoff_sum = 0.0;
  double S_cur = 0.0;

  for (int i=0; i<num_sims; i++) {
    double S_tot = S_adjust;
    S_cur = S_adjust;
    for (int j=0; j < t-1; j++){
      double gauss_bm = gaussian_box_muller();
      S_cur = S_cur * exp(sqrt(v*v*(tvec[j+1] - tvec[j]))*gauss_bm);
      S_tot += S_cur;
    }
    S_tot = S_tot / static_cast<double>(t);
    payoff_sum += std::max(S_tot - K, 0.0);
  }
  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing a European vanilla put option with a Monte Carlo method

double monte_carlo_put_price(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T) {
  double S_adjust = S * exp(T*(r-0.5*v*v));
  double S_cur = 0.0;
  double payoff_sum = 0.0;

  for (int i=0; i<num_sims; i++) {
    double gauss_bm = gaussian_box_muller();
    S_cur = S_adjust * exp(sqrt(v*v*T)*gauss_bm);
    payoff_sum += std::max(K - S_cur, 0.0);
  }

  return (payoff_sum / static_cast<double>(num_sims)) * exp(-r*T);
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Pricing an Asian vanilla Put option with a Monte Carlo method
double monte_carlo_put_price_asian(const int& num_sims, const double& S, const double& K, const double& r, const double& v, const double& T, const int& t, const vector <double>& tvec) {
  double S_adjust = S * exp(tvec[0]*(r-0.5*v*v));
  double payoff_sum = 0.0;
  double S_cur = 0.0;

  for (int i=0; i<num_sims; i++) {
    double S_tot = S_adjust;
    S_cur = S_adjust;
    for (int j=0; j < t-1; j++){
      double gauss_bm = gaussian_box_muller();
      S_cur = S_cur * exp(sqrt(v*v*(tvec[j+1] - tvec[j]))*gauss_bm);
      S_tot += S_cur;
    }
    S_tot = S_tot / static_cast<double>(t);
    payoff_sum += std::max(K - S_tot, 0.0);
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
  int t = 5;         // Number of Periods for Asian Options
  bool Asian = true; // Asian or European

  // Generate list of time periods
  if (Asian) {
    double incr = T / static_cast<double>(t);
    double tstep = 0.0;
    vector <double> tvec;
    for (int i=0; i < t; i++) {
      tstep += incr;
      tvec.push_back(tstep);
    }
    // We can also change this input to just be any given vector, but for easy
    // construction in C we do this

    // Then we calculate the call/put values via Monte Carlo
    double call = monte_carlo_call_price_asian(num_sims, S, K, r, v, T, t, tvec);
    double put = monte_carlo_put_price_asian(num_sims, S, K, r, v, T, t, tvec);

    // Finally we output the parameters and prices
    cout << "Number of Paths: " << num_sims << endl;
    cout << "Underlying:      " << S << endl;
    cout << "Strike:          " << K << endl;
    cout << "Risk-Free Rate:  " << r << endl;
    cout << "Volatility:      " << v << endl;
    cout << "Maturity:        " << T << endl;
    cout << "Periods:         " << t << endl;

    cout << "Call Price:      " << call << endl;
    cout << "Put Price:       " << put << endl;
  }
  else {
    // Then we calculate the call/put values via Monte Carlo
    double call = monte_carlo_call_price(num_sims, S, K, r, v, T);
    double put = monte_carlo_put_price(num_sims, S, K, r, v, T);

    // Finally we output the parameters and prices
    cout << "Number of Paths: " << num_sims << endl;
    cout << "Underlying:      " << S << endl;
    cout << "Strike:          " << K << endl;
    cout << "Risk-Free Rate:  " << r << endl;
    cout << "Volatility:      " << v << endl;
    cout << "Maturity:        " << T << endl;

    cout << "Call Price:      " << call << endl;
    cout << "Put Price:       " << put << endl;
  }
  return 0;
}
