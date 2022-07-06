
class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_to_cart(self, product):
        product_id = str(product.id)
        new_item = True
        if product_id not in self.cart.keys():

            self.cart[product_id] = {
                'user_id': self.request.user.id,
                'product_id': product_id,
                'title': product.title,
                'quantity': 1,
                'price': str(product.price),
                'image': product.image.url,
            }
        else:
            new_item = True
            for key, value in self.cart.items():
                if key == product_id:
                    value['quantity'] = value['quantity'] + 1
                    new_item = False
                    self.save()
                    break
            if new_item:
                self.cart[product_id] = {
                    'user_id': self.request.user.id,
                    'product_id': product_id,
                    'title': product.title,
                    'quantity': 1,
                    'price': str(product.price),
                    'image': product.image.url,
                }

        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        product_id = str(product)
        for key, value in self.cart.items():
            if key == product_id:
                value['quantity'] = value['quantity'] - 1
                if value['quantity'] < 1:
                    self.remove(product_id)
                self.save()
                break
            else:
                print('Something went wrong')

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True












""" 
Code in this file has been inspired/modified from other known works. Please ensure that
the License below is included in any of your work that is directly copied from
this source file.

MIT License

Copyright (c) [2020] [Mahmudul Hassan]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""