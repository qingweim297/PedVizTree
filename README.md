# A modular, web-based platform for interactive multi-generational pedigree visualization and genomic kinship management in perennial tree breeding programs
A complete visualization process：Users upload pedigree records and optional SNP data.  The system automatically cleans data, identifies half-sib/backcross/selfing relationships, computes the genomic relationship matrix, and generates three types of interactive visualizations: (A) pedigree network diagram, (B) G-matrix heatmap, and (C) genomic kinship clustering network.
## Features
- Interactive force-directed pedigree network supporting 10+ generations
- Real-time zoom, pan, search, filter by generation/family/provenance
- Genomic Relationship Matrix (G-matrix) heatmap with hierarchical clustering
- Side-by-side comparison of pedigree-based vs genomic-based kinship
- Color-coded nodes/edges for backcross, selfing, half-sib, and hybrid individuals
- Fully web-based (Django + Pyvis + NetworkX), no local installation needed for users
- Easily transferable to any outcrossing tree species (loblolly pine, Eucalyptus, spruce, etc.)

## Create environment
- pip install -r requirements.txt

## System Requirements
- Pthon3.9+，Django3.2.0，MySQL8.0
- ≥ 8 GB RAM for datasets > 5,000 individuals
- Modern browser (Chrome/Firefox/Edge)

## Django management script: manage.py，Database schema definition：models.py，View functions：views.py，URL routing configuration：urls.py

## Overall workflow of the ChineseFirPedV platform
<img width="576" height="700" alt="2474f606-133b-4d55-9abe-15bc5a85da9c" src="https://github.com/user-attachments/assets/eba8be4b-c1a2-4a3a-82d7-1ee786df6bf7" />

## Kinship Management System flowchart
<img width="554" height="450" alt="418f6ed9-5774-48d4-9a71-f8681433ceed" src="https://github.com/user-attachments/assets/8b4c5e24-cd6f-4dc6-8ed0-92351a13a00b" />

## Function display of genealogical diagram
<img width="538" height="303" alt="image" src="https://github.com/user-attachments/assets/1cd7ff3b-790b-42ee-9432-91bf07646cc3" />

## Heatmap of G-matrix
<img width="477" height="303" alt="image" src="https://github.com/user-attachments/assets/ae195884-2643-40f2-9b6e-f6caaf61af11" />

## Cluster diagram
<img width="486" height="235" alt="image" src="https://github.com/user-attachments/assets/e9f9d22f-552e-45b6-bdfd-629a8e95786d" />

## Global pedigree network
<img width="358" height="530" alt="image" src="https://github.com/user-attachments/assets/d86b5a99-978e-44e0-9a0b-9f4d44d4dfce" />

# Thank you for using PedVizTree!  We hope it accelerates your tree breeding program.



