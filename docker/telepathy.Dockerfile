# hivetech/intuition image
# A raring box with Intuition (https://github.com/hackliff/intuition installed
# and ready to use
# VERSION 0.1.0

# Administration
# hivetech/pyscience is an ubuntu 13.10 image with most popular python packages
FROM hivetech/intuition
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

# Install codebox ------------------------------
RUN apt-get install -y curl && \
    [ -s $HOME/.nvm/nvm.sh ] && \
    . $HOME/.nvm/nvm.sh && \
    nvm install 0.11.0 && \
    npm install -g codebox

# Install telepathy ----------------------------
RUN git clone https://github.com/hackliff/intuition-plugins.git -b master --depth 1 && \
  cd intuition-plugins/rest && \
  python setup.py install && \
  pip install honcho

# Finishing
ENTRYPOINT ["honcho", "-f", "~/.intuition/Procfile"]

# codebox on port 5100 and telpathy on 5000
EXPOSE 5000 5100
