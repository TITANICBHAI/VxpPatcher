# Render Deployment Guide

## ✅ Pre-Deployment Checklist

All files are ready for one-click deployment:

- [x] `render.yaml` - Blueprint configuration
- [x] `Dockerfile` - Container with dynamic PORT support
- [x] `requirements.txt` - Python dependencies
- [x] `app.py` - Flask application
- [x] `vxp_patcher.py` - VXP patching logic
- [x] `templates/index.html` - User interface
- [x] `.dockerignore` - Build optimization
- [x] `.gitignore` - Git configuration

## 🚀 Deploy to Render (ONE-CLICK)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "VXP Patcher for Nokia MRE phones"
git remote add origin https://github.com/YOUR_USERNAME/vxp-patcher.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [https://dashboard.render.com/](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Click **"Connect account"** (if first time) or select your account
4. Choose your **vxp-patcher** repository
5. Click **"Apply"**

**That's it!** Render will:
- ✅ Detect `render.yaml`
- ✅ Build Docker container
- ✅ Auto-generate SESSION_SECRET
- ✅ Deploy to a live URL
- ✅ Provide HTTPS automatically

### Step 3: Access Your App

After deployment (2-3 minutes), Render will give you a URL like:
```
https://vxp-patcher.onrender.com
```

## 🔧 Configuration Details

### Automatic Settings (from render.yaml)
- **Service Type:** Web Service (Docker)
- **Plan:** Free tier
- **Port:** 5000 (automatically detected)
- **Environment Variables:**
  - `SESSION_SECRET` - Auto-generated
  - `PORT` - Set to 5000

### Performance Settings (from Dockerfile)
- **Workers:** 2 Gunicorn workers
- **Timeout:** 300 seconds (5 minutes)
- **Keep-alive:** 5 seconds
- **Max upload:** 16MB

## 🔒 Security Features

- ✅ Files processed in memory only (no disk storage)
- ✅ IMSI data never stored
- ✅ Session secret auto-generated
- ✅ HTTPS enabled by default on Render
- ✅ File size limits enforced (16MB)
- ✅ File type validation (.vxp only)

## 🧪 Testing After Deployment

1. Visit your Render URL
2. Enter a test IMSI: `310260123456789`
3. Upload a .vxp file
4. Download the patched file
5. Verify file downloads correctly

## 📊 Monitoring

On Render Dashboard you can:
- View deployment logs
- Monitor app performance
- Check error rates
- Restart service if needed

## 💡 Troubleshooting

**Build fails:**
- Check Render build logs for errors
- Verify all files are committed to GitHub

**App doesn't start:**
- Check Render logs for Python errors
- Verify `requirements.txt` is complete

**Upload/download slow:**
- Normal on free tier (may sleep after inactivity)
- Consider upgrading to paid plan for better performance

**Port errors:**
- Dockerfile uses `${PORT:-5000}` for dynamic port binding
- Render automatically injects PORT environment variable

## 🎯 Success Indicators

Your deployment is successful when you see:
- ✅ Green "Live" status on Render dashboard
- ✅ App accessible via provided URL
- ✅ VXP files can be uploaded
- ✅ Patched files download correctly

## 📝 Next Steps After Deployment

1. **Custom Domain** (Optional)
   - Add custom domain in Render settings
   - Update DNS records

2. **Environment Tuning** (Optional)
   - Adjust worker count if needed
   - Monitor memory usage

3. **Monitoring** (Recommended)
   - Enable Render monitoring
   - Set up uptime checks

---

**Questions?** Check [Render Documentation](https://render.com/docs) or the app's README.md
