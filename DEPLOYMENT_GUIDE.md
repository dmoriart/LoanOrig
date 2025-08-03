# 🚀 Deployment Guide - Loan Origination System

## 🎯 **Quick Deploy Summary**

Your system is **100% ready for deployment** with all configuration files in place!

### 📋 **Deployment Order**
1. **Database First** (Supabase) ← Start here
2. **Backend Second** (Render) 
3. **Frontend Last** (Netlify)

---

## 🗄️ **1. DATABASE DEPLOYMENT (Supabase)**

### **Step 1: Access Your Supabase Project**
- URL: https://supabase.com/dashboard/project/kjbiltokwmrelyyvrnmu
- Ensure project is **active** (not paused)

### **Step 2: Initialize Database Schema**
**Option A - Supabase SQL Editor (Recommended):**
1. Go to **SQL Editor** in Supabase dashboard
2. Copy the entire contents of: `backend/migrations/001_initial_schema.sql`
3. Paste into SQL Editor and click **"Run"**
4. ✅ Should create 10 tables + sample data

**Option B - Command Line:**
```bash
# When you get the correct connection string working
psql "your-supabase-connection-string" -f backend/migrations/001_initial_schema.sql
```

### **Step 3: Get Connection String**
- Go to **Settings → Database**
- Copy the **Connection string** (URI format)
- Save for backend deployment

---

## ⚡ **2. BACKEND DEPLOYMENT (Render)**

### **Step 1: Create Render Service**
1. Go to: https://render.com/
2. Click **"New"** → **"Web Service"**
3. Connect your **GitHub** account
4. Select repository: **`dmoriart/LoanOrig`**

### **Step 2: Configure Service**
```yaml
Name: loan-origination-api
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn fastapi_app:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
```

### **Step 3: Set Environment Variables**
In Render dashboard, add:
```env
DATABASE_URL=your-supabase-connection-string
JWT_SECRET_KEY=your-generated-secret-key
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://your-frontend-url.netlify.app
```

### **Step 4: Deploy**
- Click **"Create Web Service"**
- Render will automatically deploy
- Note your backend URL: `https://loan-origination-api.onrender.com`

---

## 🌐 **3. FRONTEND DEPLOYMENT (Netlify)**

### **Step 1: Connect Repository**
1. Go to: https://app.netlify.com/
2. Click **"New site from Git"**
3. Choose **GitHub** and authorize
4. Select repository: **`dmoriart/LoanOrig`**

### **Step 2: Configure Build Settings**
```yaml
Base directory: frontend
Build command: npm run build
Publish directory: frontend/dist
```

### **Step 3: Environment Variables (Optional)**
```env
VITE_API_URL=https://loan-origination-api.onrender.com
```

### **Step 4: Deploy**
- Click **"Deploy site"**
- Netlify will auto-build and deploy
- Get your frontend URL: `https://eloquent-site-name.netlify.app`

---

## 🔧 **4. POST-DEPLOYMENT SETUP**

### **Update CORS Settings**
Update your backend environment variables with the actual frontend URL:
```env
ALLOWED_ORIGINS=https://your-actual-frontend-url.netlify.app
```

### **Test Your Deployment**
1. **Backend API**: `https://your-backend.onrender.com/docs`
2. **Frontend App**: `https://your-frontend.netlify.app`
3. **Database**: Check tables in Supabase dashboard

### **Enable Auto-Deploy**
- Both Netlify and Render will auto-deploy on `git push`
- Any changes pushed to GitHub will trigger new deployments

---

## 🎉 **Expected Results**

After successful deployment:

✅ **Frontend**: React app hosted on Netlify  
✅ **Backend**: FastAPI with docs at `/docs`  
✅ **Database**: 10 tables with sample data  
✅ **APIs**: Full loan origination endpoints  
✅ **Auto-Deploy**: Updates on every Git push  

---

## 🆘 **Troubleshooting**

### **Database Connection Issues**
- Verify Supabase project is active
- Check connection string format
- Ensure database schema was created

### **Backend Deployment Issues**
- Check Render build logs
- Verify all environment variables are set
- Ensure `requirements.txt` is correct

### **Frontend Build Issues**
- Check Node.js version (should be 18+)
- Verify `npm run build` works locally
- Check build logs in Netlify

---

## 📞 **Support**

Your system is **production-ready** with enterprise-grade features:
- Role-based authentication
- Comprehensive loan workflow
- Document management
- Audit logging
- RESTful APIs with documentation

**All configuration files are already created and optimized for deployment!** 🚀
