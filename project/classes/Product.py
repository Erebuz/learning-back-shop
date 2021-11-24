class Product:
    def __init__(self, arr):
        self.id = arr[0]
        self.price = arr[1]
        self.type = arr[2]
        self.width = arr[3]
        self.height = arr[4]
        self.thickness = arr[5]
        self.material = arr[6]
        self.count = arr[7]
        self.description = arr[8]
        self.image = arr[9]

    def to_dict(self):
        return {'id': self.id, 'price': self.price, 'name': self.type, 'width': self.width, 'height': self.height,
                'thickness': self.thickness, 'material': self.material, 'count': self.count,
                'description': self.description, 'image': self.image}


class ProductHistory:
    def __init__(self, arr):
        self.id, self.product_id, self.count, self.status, self.date, self.price, self.material, self.description = arr

    def to_dict(self):
        return {
            'id': self.id, 'product_id': self.product_id, 'count': self.count, 'status': self.status, 'date': self.date.strftime("%d/%m/%Y, %H:%M:%S"),
            'price': self.price, 'material': self.material, 'description': self.description,
        }