#! /bin/bash

echo "writing database config ($DB_USERNAME:$DB_PASSWORD@$DB_HOST)"
cat > /app/config/database.yml << EOF
default: &mysql
  adapter: mysql2
  pool: 5
  timeout: 5000
  host: ${DB_HOST}
  username: ${DB_USERNAME}
  password: ${DB_PASSWORD}

development:
  <<: *mysql
  database: team_dashboard_development

test:
  <<: *mysql
  database: team_dashboard_test

production:
  <<: *mysql
  database: team_dashboard_production
EOF

cd /app
rake db:create && rake db:migrate
if [ -n "$POPULATE" ]; then
  rake populate
fi

rails server
