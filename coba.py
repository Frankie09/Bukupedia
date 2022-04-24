from cryptography.fernet import Fernet


decMessage = fernet.decrypt('99048f2bff98e18d5fbd85470a6c9194').decode()