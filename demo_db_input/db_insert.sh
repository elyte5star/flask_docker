mongoimport --db elyte_admin --collection products  ./data/products.json
mongoimport --db elyte_admin --collection users ./data/valid_user.json
mongosh elyte_admin ./data/db_user.js
