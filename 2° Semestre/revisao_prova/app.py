from models import User, Product
from database import Base, engine, session

Base.metadata.create_all(bind=engine)

#adicao de usuario



#session.begin()
#user = User(nome='zefinha', email='bil@bilzin')
#session.add(user)  
#user = User(nome='josafa', email='josafa@junho')
#session.add(user)
# user = User(nome='pelezin', email='reidadama123@')
# session.add(user)

# session.commit()
# session.close()

#adicaçõ de produtos

# session.begin()

# product = Product(nome="sabonete", valor=500.0, user_id=1)
# # product.user_id = 1
# session.add(product)
# product = Product(nome="feijão", valor=500.0, user_id=1)
# # product.user_id = 1
# session.add(product)
# product = Product(nome="agua sanitária", valor=500.0, user_id=1)
# # product.user_id = 1
# session.add(product)
# product = Product(nome="coloral", valor=500.0, user_id=1)
# # product.user_id = 1
# session.add(product)


# product = Product(nome="capim santo", valor=500.0, user_id = 2)
# # product.user_id = 2
# session.add(product)
# product = Product(nome="erva cidreira", valor=500.0, user_id = 2)
# # product.user_id = 2
# session.add(product)

# session.commit()

# session.close()


session.begin()

user = session.query(User).where(User.id == 1).first()

for prod in user.produtos:
    print(prod.user.nome)
    print(prod.nome)

session.close()


