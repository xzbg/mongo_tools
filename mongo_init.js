
use admin;
db.createUser({
    user: "user_admin",
    pwd: "1DG0*a7p_l",
    roles: [
        { role: "userAdminAnyDatabase", db: "admin" }
    ]
});

db.createUser({
    user: "db_reader",
    pwd: "k*_jZ2J0RV",
    roles: [
        { role: "readAnyDatabase", db: "admin" }
    ]
});

db.createUser({
    user: "P32",
    pwd: "awZC3_74Tr",
    roles: [
        { role: "readWrite", db: "P32" },
        { role: "dbAdmin", db: "P32" }
    ]
});

db.createUser({
    user: "P32_CENTER",
    pwd: "2Qc*LQgis9",
    roles: [
        { role: "readWrite", db: "P32_CENTER" },
        { role: "dbAdmin", db: "P32_CENTER" }
    ]
});
    