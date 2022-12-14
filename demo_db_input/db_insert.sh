mongoimport --db visma_admin --collection products  ./data/products.json
mongoimport --db visma_admin --collection users ./data/valid_user.json
mongosh visma_admin ./data/db_user.js
