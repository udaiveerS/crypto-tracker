# crypto-tracker

Crypto-tracker Python library for tracking key data (social/price/wallets) for alpha

## Track Twitter follows of key accounts (SMEs) [:heavy_check_mark:]
- can get early view of projects launching
- track trends and group follows across multiple days

## Track specific coins from Coin Geko [:heavy_multiplication_x:]
- Make custom indices of coins 
- Track volumes to catch sector rotations  

## Track wallet evens with nansen [:heavy_multiplication_x:]
- Alerts for when whales distribute tokens in profolio  
- Discover new unlisted coins 

This is a standard Dganjo project python > 3.6.4  

Current commands are supported, a SQL db is required to store data 
```python

# Track a user and metrics 
python manage.py track_new_user --username pierskicks

# Track new follows 
python manage.py fetch_followers    


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
