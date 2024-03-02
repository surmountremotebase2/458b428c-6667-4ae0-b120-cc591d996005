from surmount.base_class import Strategy, TargetAllocation
from surmount.data import CompanyLeadershipData

class TradingStrategy(Strategy):
    def __init__(self):
        # A predefined list of tickers you're interested in
        self.tickers = ["APPL", "MSFT", "GOOGL", "AMZN"]

    @property
    def assets(self):
        # The assets we're considering for trading
        return self.tickers

    @property
    def interval(self):
        # Assuming daily analysis is sufficient for our needs
        return "1day"

    @property
    def data(self):
        # Assuming CompanyLeadershipData takes a ticker and returns
        # data class instance with information on company leadership composition
        return [CompanyLeadershipData(ticker) for ticker in self.tickers]

    def run(self, data):
        # Initialize an empty allocation dictionary
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Fetch the data for each company. Assuming CompanyLeadershipData
            # provides a .female_percentage attribute that gives us the
            # percentage of female leadership.
            female_leadership_percentage = data[CompanyLeadershipData(ticker)].female_percentage
            
            # Example strategy: Invest proportionally to the percentage of female leadership.
            # This simplistic allocation assigns more weight to companies with higher 
            # female leadership percentages. The actual allocation in a real fund might need
            # normalization or capping based on risk management principles.
            # The example assumes female_leadership_percentage is a value between 0 and 100.
            # Conversion to a fraction of 1 for allocation.
            allocation_dict[ticker] = female_leadership_percentage / 100
        
        # Normalize allocations to ensure the sum does not exceed 1
        total_allocation_percentage = sum(allocation_dict.values())
        normalized_allocation_dict = {ticker: allocation / total_allocation_percentage for ticker, allocation in allocation_dict.items()}

        return TargetAllocation(normalized_allocation_dict)