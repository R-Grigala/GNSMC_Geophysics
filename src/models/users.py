import uuid

from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models.base import BaseModel

# ONE - TO - ONE relationship
class User(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, default=lambda: str(uuid.uuid4().hex)[:12])
    name = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)

    # One-to-One relationship with Role
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship("Role", back_populates="user", uselist=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def check_permission(self, request):
        permisions = [getattr(permision, request) for permision in self.role]
        return any(permisions)

    def is_admin(self):
        return any(role.name == "admin" for role in self.role)

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"
    

class Role(db.Model, BaseModel):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    can_geohysic = db.Column(db.Boolean, default=False)
    can_geologic = db.Column(db.Boolean, default=False)
    can_hazard = db.Column(db.Boolean, default=False)
    can_geodetic = db.Column(db.Boolean, default=False)

    # One-to-One relationship with User
    user = db.relationship("User", back_populates="role", uselist=False)

    def __repr__(self):
        return f"{self.name}"