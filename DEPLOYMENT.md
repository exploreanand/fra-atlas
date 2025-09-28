# FRA Atlas - Deployment Guide

## 🚀 Railway Deployment (Recommended)

### Prerequisites
- GitHub repository with your code
- Railway account (free tier available)
- GeoServer instance (can be on separate server)

### Step 1: Prepare Your Repository
1. Ensure all production files are committed:
   - `Dockerfile`
   - `requirements.txt`
   - `Procfile`
   - `railway.toml`
   - Updated `settings.py`
   - `.gitignore`

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect the Dockerfile

**Note**: If you encounter GDAL version conflicts during Docker build, you have two alternative Dockerfiles:
- `Dockerfile.simple` - Uses Ubuntu base with system GDAL
- `Dockerfile.alternative` - Uses kartoza/django base image

To use an alternative Dockerfile, rename it to `Dockerfile` before deploying.

### Step 3: Add PostgreSQL Database
1. In your Railway project, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically provide `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables
In Railway → Variables, add:

```bash
# Required
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app
GEOSERVER_URL=https://your-geoserver-domain.com/geoserver

# Optional
ADMIN_PASSWORD=your-admin-password
```

### Step 5: Enable PostGIS
1. Go to Railway → Data → PostgreSQL
2. Open the database console
3. Run these SQL commands:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

### Step 6: Deploy
1. Railway will automatically build and deploy
2. Check the logs for any errors
3. Visit your app URL to verify it's working

## 🔧 Alternative Deployment Options

### AWS Elastic Beanstalk
1. Create EB application
2. Use Docker platform
3. Configure RDS PostgreSQL with PostGIS
4. Set environment variables in EB console

### DigitalOcean App Platform
1. Connect GitHub repository
2. Use Docker buildpack
3. Add managed PostgreSQL database
4. Configure environment variables

### Heroku (Limited - No PostGIS)
1. Use Heroku Postgres (no PostGIS support)
2. Consider using external PostGIS database
3. Deploy using Heroku CLI or GitHub integration

## 🗺️ GeoServer Setup

### Option 1: Separate Server
- Deploy GeoServer on AWS EC2, DigitalOcean, or similar
- Upload your shapefiles and TIFF files
- Configure CORS for cross-origin requests
- Update `GEOSERVER_URL` in your Django app

### Option 2: Railway Service
- Create separate Railway service for GeoServer
- Use Java buildpack
- Add persistent volume for data storage

### Option 3: Docker Compose (Local Development)
```yaml
version: '3.8'
services:
  geoserver:
    image: kartoza/geoserver:latest
    ports:
      - "8080:8080"
    environment:
      - GEOSERVER_ADMIN_PASSWORD=geoserver
    volumes:
      - geoserver_data:/opt/geoserver/data_dir
```

## 🔒 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY`
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enabled (Railway provides automatically)
- [ ] Database credentials secured
- [ ] GeoServer secured with authentication
- [ ] Static files served via CDN (Railway handles this)

## 📊 Monitoring

### Railway
- Built-in metrics and logs
- Health checks configured
- Automatic restarts on failure

### Custom Monitoring
- Add Sentry for error tracking
- Use New Relic or DataDog for performance monitoring
- Set up log aggregation with ELK stack

## 🚨 Troubleshooting

### Common Issues

1. **GDAL version conflicts**: 
   - Error: "Python bindings of GDAL X.X.X require at least libgdal X.X.X, but X.X.X was found"
   - Solution: Use `Dockerfile.simple` or `Dockerfile.alternative` instead
   - Alternative: Remove GDAL from requirements.txt and let it auto-detect

2. **Database connection**: Check `DATABASE_URL` format
3. **Static files**: Verify WhiteNoise configuration
4. **GeoServer CORS**: Enable CORS in GeoServer settings
5. **Memory issues**: Increase Railway plan or optimize queries

### Debug Commands
```bash
# Check logs
railway logs

# Run Django shell
railway run python manage.py shell

# Check database
railway run python manage.py dbshell

# Collect static files
railway run python manage.py collectstatic
```

## 📈 Scaling

### Railway
- Upgrade to Pro plan for more resources
- Use multiple workers for high traffic
- Add Redis for caching

### Database
- Use read replicas for heavy read workloads
- Implement database connection pooling
- Consider database sharding for large datasets

## 🔄 CI/CD

### GitHub Actions
```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway-app/railway-deploy@v1
        with:
          railway-token: ${{ secrets.RAILWAY_TOKEN }}
```

## 📞 Support

- Railway Documentation: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- PostGIS Documentation: https://postgis.net/documentation/
- GeoServer Documentation: https://docs.geoserver.org/
