user_data = [
    {
        "email": "asrour@ciatek.net",
        "firstName": "Abbas",
        "lastName": "Srour",
        "role": "ADMINISTRATOR",
        "phone": "+961 71427429",
        "password": "Ciatek@123"
    },
    {
        "email": "johndoe1@domain.com",
        "firstName": "John",
        "lastName": "Doe",
        "role": "ADMINISTRATOR",
        "phone": "+1 202-918-2132",
        "password": "TestPassword@123"
    },
    {
        "email": "johndoe2@domain.com",
        "firstName": "John",
        "lastName": "Doe",
        "role": "AUDITOR",
        "phone": "+1 472-202-9946",
        "password": "TestPassword@123"
    },
    {
        "email": "johndoe3@domain.com",
        "firstName": "John",
        "lastName": "Doe",
        "role": "MINISTRY_EMPLOYEE",
        "phone": "+1 505-644-0118",
        "password": "TestPassword@123"
    },
    {
        "email": "johndoe4@domain.com",
        "firstName": "John",
        "lastName": "Doe",
        "role": "FIRM_EMPLOYEE",
        "phone": "+1 472-236-0568",
        "password": "TestPassword@123"
    },
    {
        "email": "johndoe5@domain.com",
        "firstName": "John",
        "lastName": "Doe",
        "role": "ADMINISTRATOR",
        "phone": "+355 69 275 6526",
        "password": "TestPassword@123"
    },
    {
        "email": "janedoe2@domain.com",
        "firstName": "Jane",
        "lastName": "Doe",
        "role": "AUDITOR",
        "phone": "+355 68 505 3865",
        "password": "TestPassword@123"
    },
    {
        "email": "billsmith3@domain.com",
        "firstName": "Bill",
        "lastName": "Smith",
        "role": "MINISTRY_EMPLOYEE",
        "phone": "+355 69 963 2732",
        "password": "TestPassword@123"
    },
    {
        "email": "alicedavis4@domain.com",
        "firstName": "Alice",
        "lastName": "Davis",
        "role": "FIRM_EMPLOYEE",
        "phone": "+355 67 765 3243",
        "password": "TestPassword@123"
    },
    {
        "email": "markwilson5@domain.com",
        "firstName": "Mark",
        "lastName": "Wilson",
        "role": "ADMINISTRATOR",
        "phone": "+961 3 342 005",
        "password": "TestPassword@123"
    },
    {
        "email": "susanlee6@domain.com",
        "firstName": "Susan",
        "lastName": "Lee",
        "role": "AUDITOR",
        "phone": "+961 3 688 039",
        "password": "TestPassword@123"
    },
    {
        "email": "johndoehuang7@domain.com",
        "firstName": "John",
        "lastName": "Huang",
        "role": "MINISTRY_EMPLOYEE",
        "phone": "+961 79 323 964",
        "password": "TestPassword@123"
    },
    {
        "email": "katejohnson8@domain.com",
        "firstName": "Kate",
        "lastName": "Johnson",
        "role": "FIRM_EMPLOYEE",
        "phone": "+961 78 903 530",
        "password": "TestPassword@123"
    },
    {
        "email": "robertmiller9@domain.com",
        "firstName": "Robert",
        "lastName": "Miller",
        "role": "ADMINISTRATOR",
        "phone": "+961 76 474 693",
        "password": "TestPassword@123"
    },
    {
        "email": "emilywilliams10@domain.com",
        "firstName": "Emily",
        "lastName": "Williams",
        "role": "AUDITOR",
        "phone": "+961 79 321 211",
        "password": "TestPassword@123"
    },
    {
        "email": "michaelrodriguez11@domain.com",
        "firstName": "Michael",
        "lastName": "Rodriguez",
        "role": "MINISTRY_EMPLOYEE",
        "phone": "+961 79 324 099",
        "password": "TestPassword@123"
    },
    {
        "email": "sophiagarcia12@domain.com",
        "firstName": "Sophia",
        "lastName": "Garcia",
        "role": "FIRM_EMPLOYEE",
        "phone": "+961 79 319 631",
        "password": "TestPassword@123"
    },
    {
        "email": "williamjones13@domain.com",
        "firstName": "William",
        "lastName": "Jones",
        "role": "ADMINISTRATOR",
        "phone": "+961 3 466 437",
        "password": "TestPassword@123"
    },
    {
        "email": "emilymartinez14@domain.com",
        "firstName": "Emily",
        "lastName": "Martinez",
        "role": "AUDITOR",
        "phone": "+961 79 164 031",
        "password": "TestPassword@123"
    },
    {
        "email": "davidwilson15@domain.com",
        "firstName": "David",
        "lastName": "Wilson",
        "role": "MINISTRY_EMPLOYEE",
        "phone": "+961 3 308 772",
        "password": "TestPassword@123"
    },
    {
        "email": "oliviajohnson16@domain.com",
        "firstName": "Olivia",
        "lastName": "Johnson",
        "role": "FIRM_EMPLOYEE",
        "phone": "+961 76 962 214",
        "password": "TestPassword@123"
    },
    {
        "email": "jamesbrown17@domain.com",
        "firstName": "James",
        "lastName": "Brown",
        "role": "ADMINISTRATOR",
        "phone": "+961 3 670 636",
        "password": "TestPassword@123"
    },
    {
        "email": "emilythomas18@domain.com",
        "firstName": "Emily",
        "lastName": "Thomas",
        "role": "AUDITOR",
        "phone": "+961 79 322 561",
        "password": "TestPassword@123"
    },
    {
        "email": "josephhernandez19@domain.com",
        "firstName": "Joseph",
        "lastName": "Hernandez",
        "role": "MINISTRY_EMPLOYEE",
        "phone": "+961 3 819 678",
        "password": "TestPassword@123"
    },
    {
        "email": "ameliasmith20@domain.com",
        "firstName": "Amelia",
        "lastName": "Smith",
        "role": "FIRM_EMPLOYEE",
        "phone": "+961 79 322 171",
        "password": "TestPassword@123"
    },
]

test_emails = [
    "asrour@ciatek",  # No .net
    "asrour.net",  # No @
    "asrour@.net",  # No domain
    "asrour@ciatek.",  # No extension
    "@ciatek.net",  # No username
    "asrour@ciatek..net",  # Double dot
]

test_passwords = [
    "Ciatek123",  # No Special Character
    "Ciatek@12345678901234567890123456789012345678901234567890123456789012345678901234567890",  # Too Long
    "Cia@1",  # Too Short
    "Ciatekasd@",  # No Number
]

test_names = [
    "Abbas123",  # Number
    "Abbas@",  # Special Character
    "Abbas ",  # Space
    "Abbas.",  # Dot
    "Abbas-",  # Dash
    "Abbas_",  # Underscore
    "Abbas/",  # Slash
    "Abbas\\",  # Backslash
    "Abbas*",  # Asterisk
    "Abbas+",  # Plus
    "Abbas=",  # Equal
    "Abbas!",  # Exclamation
    "Abbas?",  # Question
    "Abbas#",  # Hash
    "Abbas$",  # Dollar
    "Abbas%",  # Percent
    "Abbas^",  # Caret
    "Abbas&",  # Ampersand
    "Abbas(",  # Open Parenthesis
    "Abbas)",  # Close Parenthesis
    "Abbas[",  # Open Bracket
    "Abbas]",  # Close Bracket
    "Abbas{",  # Open Brace
    "Abbas}",  # Close Brace
    "Abbas<",  # Open Angle
    "Abbas>",  # Close Angle
    "Abbas|",  # Pipe
    "Abbas~",  # Tilde
    "Abbas`",  # Backtick
    "Abbas;",  # Semicolon
    "Abbas:",  # Colon
    "Abbas'",  # Single Quote
    "Abbas\"",  # Double Quote
    "Abbas,",  # Comma
    "Abbas.",  # Period
    "",  # Empty
    " ",  # Space
    "aasdasdasdasdadasdadasdasdasdasdasddddddddddddddddddddddddddddddddddddddd"  # Too Long
]
