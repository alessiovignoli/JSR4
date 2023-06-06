#FROM python:3.9.16-slim
FROM suzannejin/3dtf:python3
LABEL maintainer="Alessio Vignoli" \
        name="suzannejin/3dtf:sr_jaspar" \
        description="Docker image containing JASPAR inference tool and dependencies" 

RUN pip install \
        biopython==1.76 \
        certifi==2022.9.24 \
        charset_normalizer==2.1.1 \
        click==8.1.3 \
		coreapi==2.3.3 \
		coreapi-cli==1.0.9 \
        coreschema==0.0.4 \
        gitdb==4.0.1 \
        GitPython==3.1.29 \
        idna==3.4 \
        itypes==1.2.0 \
        Jinja2==3.1.2 \
        MarkupSafe==2.1.1 \
        ProDy==2.2.0 \
        requests==2.28.1 \
        smmap==3.0.1 \
        tqdm==4.64.1 \
        uritemplate==4.1.1 \
        urllib3==1.26.12

# install blast+ 2.13.0
RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz \
    && tar -xf ncbi-blast-2.13.0+-x64-linux.tar.gz  \
    && mv ncbi-blast-2.13.0+/bin/* /usr/bin/ \
    && rm -r ncbi-blast-2.13.0+

# install hmmer 3.2.1
RUN apt-get update \
    && apt-get install -y hmmer \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/*

# copying the forked git repo of sr jaspar
WORKDIR /usr/local/
RUN git clone https://github.com/alessiovignoli/JASPAR-SR.git \
	&& cd JASPAR-SR/ \
	&& git checkout 1254e29395882a051889ae303764a1f137cffef4
