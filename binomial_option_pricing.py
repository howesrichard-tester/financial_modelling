import numpy as np

def binomial_option_price(S, K, T, r, sigma, N, option_type='call'):
    """
    Calculate the price of an option using the binomial model.
    
    Parameters:
    -----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate (annual)
    sigma : float
        Volatility of the underlying stock (annual)
    N : int
        Number of time steps in the binomial tree
    option_type : str
        Type of option ('call' or 'put')
    
    Returns:
    --------
    float
        Option price
    """
    # Calculate parameters
    dt = T/N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt) - d)/(u - d)
    
    # Initialize stock price tree
    stock = np.zeros((N+1, N+1))
    stock[0,0] = S
    
    # Generate stock price tree
    for i in range(1, N+1):
        stock[i,0] = stock[i-1,0] * u
        for j in range(1, i+1):
            stock[i,j] = stock[i-1,j-1] * d
    
    # Initialize option value array
    option = np.zeros((N+1, N+1))
    
    # Calculate option values at expiration
    for j in range(N+1):
        if option_type.lower() == 'call':
            option[N,j] = max(0, stock[N,j] - K)
        else:  # put option
            option[N,j] = max(0, K - stock[N,j])
    
    # Calculate option values at earlier nodes by backwards induction
    for i in range(N-1, -1, -1):
        for j in range(i+1):
            option[i,j] = np.exp(-r*dt) * (p*option[i+1,j] + (1-p)*option[i+1,j+1])
    
    return option[0,0]

def get_implied_volatility(target_price, S, K, T, r, N, option_type='call', 
                         tolerance=1e-5, max_iter=100):
    """
    Calculate implied volatility using the binomial model and Newton's method.
    
    Parameters:
    -----------
    target_price : float
        Market price of the option
    S, K, T, r, N : float
        Same as in binomial_option_price function
    option_type : str
        Type of option ('call' or 'put')
    tolerance : float
        Convergence tolerance
    max_iter : int
        Maximum number of iterations
    
    Returns:
    --------
    float
        Implied volatility
    """
    sigma = 0.2  # Initial guess
    for i in range(max_iter):
        price = binomial_option_price(S, K, T, r, sigma, N, option_type)
        diff = price - target_price
        
        if abs(diff) < tolerance:
            return sigma
        
        # Calculate numerical derivative
        h = 0.0001
        price_up = binomial_option_price(S, K, T, r, sigma + h, N, option_type)
        vega = (price_up - price) / h
        
        # Newton's method update
        sigma = sigma - diff/vega
        
        # Ensure sigma stays positive
        if sigma <= 0:
            sigma = 0.0001
            
    raise ValueError("Implied volatility calculation did not converge")

# Example usage:
if __name__ == "__main__":
    # Example parameters
    S = 100  # Current stock price
    K = 100  # Strike price
    T = 1.0  # Time to maturity (1 year)
    r = 0.05  # Risk-free rate (5%)
    sigma = 0.2  # Volatility (20%)
    N = 100  # Number of time steps
    
    # Calculate call and put option prices
    call_price = binomial_option_price(S, K, T, r, sigma, N, 'call')
    put_price = binomial_option_price(S, K, T, r, sigma, N, 'put')
    
    print(f"Call option price: ${call_price:.2f}")
    print(f"Put option price: ${put_price:.2f}")
