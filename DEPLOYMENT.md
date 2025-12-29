# Guardian Keychain - Production Deployment Guide

## HTTPS Configuration

### Option 1: Using Firebase App Hosting (Recommended)
Your app is already configured with Firebase App Hosting. It automatically provides HTTPS out of the box.

**Steps:**
1. Deploy using Firebase CLI: `firebase deploy`
2. Your app will be available at: `https://[project-id].web.app`

### Option 2: Using Vercel
Vercel automatically provides free HTTPS for all deployments.

**Steps:**
1. Push your code to GitHub
2. Import project in Vercel Dashboard
3. Vercel auto-configures HTTPS
4. Your app is live at: `https://[project-name].vercel.app`

### Option 3: Using Azure App Service
Deploy to Azure App Service with built-in HTTPS support.

**Steps:**
```bash
# Install Azure CLI
# Login to Azure
az login

# Create resource group
az group create --name kid-safety-rg --location eastus

# Create App Service Plan
az appservice plan create --name kid-safety-plan --resource-group kid-safety-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group kid-safety-rg --plan kid-safety-plan --name kid-safety-app --runtime "node|18-lts"

# Deploy
az webapp deployment source config-zip --resource-group kid-safety-rg --name kid-safety-app --src ./deploy.zip
```

### Option 4: Using Docker + NGINX Reverse Proxy

See `docker-compose.yml` for containerized deployment with SSL.

## Local HTTPS Testing

To test HTTPS locally:

```bash
# 1. Generate self-signed certificates (Windows PowerShell)
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "cert:\CurrentUser\My"

# 2. Export to PEM format (needs OpenSSL)
openssl req -new -x509 -keyout server.key -out server.crt -days 365 -nodes

# 3. Run with HTTPS
npm run start:https
```

## Environment Variables

Create `.env.local` for local development:

```
NEXT_PUBLIC_API_URL=https://localhost:3000
NEXT_PUBLIC_APP_NAME=Guardian Keychain
FIREBASE_PROJECT_ID=your-project-id
```

For production (in `apphosting.yaml`):

```yaml
runConfig:
  maxInstances: 1
  environmentVariables:
    NODE_ENV: production
    NEXT_PUBLIC_API_URL: https://your-domain.com
```

## Security Headers

HTTPS headers are automatically configured in `next.config.ts`:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

## Domain Setup

To use your own domain:

1. **Purchase domain** from registrar (GoDaddy, Namecheap, etc.)
2. **Update DNS records** to point to your hosting provider
3. **Set up SSL certificate** (automatic with most platforms)
4. **Update environment variables** with your domain

## Monitoring

Monitor your deployment with:
- Firebase Console: https://console.firebase.google.com
- Application Logs: Check deployment logs in Firebase Console
- Performance: Monitor real-time metrics

## Troubleshooting

### Mixed Content Warning
Ensure all resources (images, APIs) are served over HTTPS, not HTTP.

### SSL Certificate Issues
- Verify domain is correctly configured
- Check DNS propagation
- Certificate renewal is automatic with most providers

### Port Issues
- Make sure port 443 (HTTPS) is allowed in firewall
- Cloud providers typically handle port mapping automatically

## Production Checklist

- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Environment variables set
- [ ] Database connections secure
- [ ] API endpoints use HTTPS
- [ ] CSP headers configured
- [ ] Rate limiting enabled
- [ ] Error logging configured
- [ ] Performance monitoring enabled
- [ ] Backup and disaster recovery plan
