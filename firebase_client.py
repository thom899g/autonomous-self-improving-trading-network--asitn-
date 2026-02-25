"""
Firebase Client for ASITN state management
Handles all database operations with proper error handling
"""
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

from config import config

class FirebaseClient:
    """Firebase Firestore client with error handling and type safety"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        try:
            # Initialize Firebase
            if not firebase_admin._apps:
                cred = credentials.Certificate(config.firebase.credentials_path)
                firebase_admin.initialize_app(cred, {
                    'projectId': config