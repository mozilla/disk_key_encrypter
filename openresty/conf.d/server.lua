-- lua-resty-openidc options

-- See also https://github.com/zmartzone/lua-resty-openidc#sample-configuration-for-google-signin for more options

opts = {
  redirect_uri_path = "/redirect_uri",
  discovery = "https://auth.mozilla.auth0.com/.well-known/openid-configuration",
  -- client_id = "",
  -- client_secret = "",
  iat_slack = 600,
  redirect_uri_scheme = "https",
  logout_path = "/logout",
  redirect_after_logout_uri = "https://sso.mozilla.com/forbidden",
  -- The following options are used to verify a user session should be kept running and that the user is still valid
  -- refresh_session_interval will 302 the user's browser every X amount of seconds (here, 900) transparently
  -- renew_access_token_on_expiry will use an access or refresh token with a server-side request. If you use the later
  -- make sure you enable all 3 options: renew_access_token_on_expiry, access_token_expires_in, access_token_expires_leeway
  -- or understand the consequences of not doing so.
  --
  --renew_access_token_on_expiry = true
  --access_token_expires_in = 900,
  --access_token_expires_leeway = 60,
  -- If using renew_access_token_on_expiry you may need a specific scope to request a refresh token
  --scope = "openid email profile offline_access",
  scope = "openid email profile",
  refresh_session_interval = 900,
  proxy_opts = {
   http_proxy  = "http://proxy.dmz.mdc1.mozilla.com:3128/",
   https_proxy = "http://proxy.dmz.mdc1.mozilla.com:3128/"
  }
}
