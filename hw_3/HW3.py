#!/usr/bin/env python
# coding: utf-8

# # Homework 3
# ## DS 3000: Foundation of Data Science
# Name: Vivian Shu Yi Li <br>
# NUID: 001506227 <br>
# Date: June 11, 2023 <br>

# In[1]:


# load libraries
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from collections import Counter


# In[2]:


# connecting to SQLite database
con = sqlite3.connect('genetics.db')


# ## Question 1
# - how many gene-disease association were cataloged
# - how many total papers were published between 1960 and the present year

# In[3]:


# write the query
q1 = """select count(*) as n_association, sum(num_pubs) as n_publication, last_year as year 
        from disgenet 
        where last_year >= 1960
        group by last_year
        order by last_year"""


# In[4]:


# connect & get df
df_count = pd.read_sql_query(q1, con)

# delete the unneccesary rows
df_count = df_count[(df_count['year'] != 'NA') & (df_count['year'] != 'last_year')]

# show df
df_count.head(10)


# In[5]:


# find the total of association & publication
total_assoc = int(df_count['n_association'].sum())
total_pub = int(df_count['n_publication'].sum())

# print result
print("Total gene-disease associations:", total_assoc, "associations")
print("Total published papers:", total_pub, "publications")


# In[6]:


# plot cumulative total(using cumsum)
plt.figure(figsize=(10, 7))
plt.plot(df_count['year'], df_count['n_publication'].cumsum(), label='Cumulative Publications', color='mediumpurple')
plt.plot(df_count['year'], df_count['n_association'].cumsum(), label='Cumulative Associations', color='steelblue')
plt.axvline(x=2003, color='palevioletred', label='2003 Human Genome Project')

# label the plot
plt.xlabel('Year')
plt.ylabel('Cumulative Count')
plt.title('Cumulative Number of Associations and Published Papers (1960 - Present)')
plt.legend()
plt.grid(alpha=0.4)
plt.show()


# ### Human Genome Project
# The Human Genome Project's 2003 completion led to a surge in gene-disease association research. As the years get closer to the present time, the cumulative number of publication increases.
# 
# As shown in the line plot above, the number of publications and associations remained relatively low and consistent from 1960 to the late 1990s. However, after the release of the Human Genome Project, the cumulative number of publications rise exponentially within two decades. Although the cumulative number of associations has increased, it remained lower than the cumulative publication count. This demonstrates that the human genome and related topics gained popularity as more researchers became interested in them. Thus, they began to research genes (and other related topics) to delve deeper into the understanding of genes and their association with diseases. 
# 
# The increase in gene-disease research implies that the significance of genetics in unraveling the causes of disease has become widely acknowledged. Overall, the Human Genome Project served as a catalyst for the growth of gene-disease association research.

# ## Question 2
# - What genes have the greatest number of associations
# - What diseases have the most number of associations

# In[7]:


# write the query
q2 = """ select gene_symbol, gene_name, count(*) as n_association, sum(num_pubs) as n_publication
    from disgenet 
    group by gene_symbol
    order by n_association DESC 
    limit 10"""

# connect & show df
df_gene = pd.read_sql_query(q2, con)
df_gene


# In[8]:


# write query
q2_5 = """select disease_name, count(*) as n_association, sum(num_pubs) as n_publication
            from disgenet 
            where disease_type != 'group'
            group by disease_name
            order by n_association DESC 
            limit 10"""

# connect & show df
df_disease = pd.read_sql_query(q2_5, con)
df_disease


# ## Question 3
# - plot the degree distribution of genes on a log-log scale to show it is scale free distribution

# In[9]:


# write query
q3 = """ select count(*) as g_association, degree_gene
from (select gene_symbol, count(*) as degree_gene
from disgenet 
group by gene_symbol
order by degree_gene DESC)
group by degree_gene
order by degree_gene
"""
# connect & get df
df_g_degree = pd.read_sql_query(q3, con)
df_g_degree


# In[10]:


# write query
q3_5 = """ select count(*) as d_association, degree_disease
from (select disease_name, count(*) as degree_disease
from disgenet 
group by disease_name
order by degree_disease DESC)
group by degree_disease
order by degree_disease
"""
# connect & get df
df_d_degree = pd.read_sql_query(q3_5, con)
df_d_degree


# In[11]:


# Plot the degree distributions 
plt.figure(figsize=(10, 7))
plt.scatter(np.log10(df_g_degree['degree_gene']), np.log10(df_g_degree['g_association']), 
            s=8, label='Genes', color='salmon', alpha=0.5)
plt.scatter(np.log10(df_d_degree['degree_disease']), np.log10(df_d_degree['d_association']), 
            s=8, label='Diseases', color='orchid', alpha = 0.5)

# label the plot 
plt.xlabel('Degree (log10)')
plt.ylabel('Count (log10)')
plt.title('Degree Distributions of Genes & Diseases vs Number of Genes & Diseases')
plt.legend()
plt.grid(alpha=0.4)
plt.show()


# ## Question 4
# - identify the 300+ genes strongly associated w/ Alzhemier's Disease
#     - EI >= 0.667
#     - num of publications >= 11

# In[12]:


# write query
q4 = """select gene_symbol, num_pubs, EI
        from disgenet 
        where disease_name LIKE "Alzheimer's Disease"
        and EI >= 0.667 and num_pubs >= 11
        group by gene_symbol
        order by num_pubs desc"""

# connect & show df (top 10)
df_alz = pd.read_sql_query(q4, con)
df_alz.head(10)


# ## Question 5
# - plot Disease Pllleiotrophy Index (DPI) vs Disease Specificity Index (DSI)

# In[13]:


# write query 
q5 = """select gene_symbol, num_pubs, EI, DSI, DPI
    from disgenet 
    where disease_name LIKE "Alzheimer's Disease"
    and EI >= 0.667 and num_pubs >= 11
    group by gene_symbol
    order by num_pubs desc"""

# connect & show df
df_plot = pd.read_sql_query(q5, con)
df_plot


# In[14]:


# find the gene_symbol w/ greatest DSI (top 5)
df_plot.sort_values(by='DSI', ascending=False).head(5)


# In[15]:


# plot the scatter plot
plt.figure(figsize=(12, 15))
plot = plt.scatter(df_plot.DSI, df_plot.DPI, c=df_plot['EI'], 
                   s=df_plot.num_pubs, cmap='viridis')

# plot text based on DSI & DPI shown in dataframe
plt.text(0.338, 0.962, 'APOE', fontsize=12)
plt.text(0.422, 0.846, 'APP', fontsize=12)
plt.text(0.445, 0.923, 'MAPT', fontsize=12)
plt.text(0.769, 0.269, 'CALHM1', fontsize=12)
# add note for the marker size
plt.text(0.3, 0.2, "note: markersize is based on number of publications")

# label
plt.xlabel('Disease Specificity Index (DSI)', fontsize=14)
plt.ylabel('Disease Pleiotrophy Index (DPI)', fontsize=14)
plt.colorbar(plot, label='Evidence Index (EI)')
plt.title('DSI vs DPI', fontsize=14)
plt.grid(alpha=0.4)
plt.show()


# ## Question 6
# - what biological processes are these Alzheimer's linked genes most frequently in?

# In[16]:


# write query
q6 = """select distinct go_id, count(go_id) as n_gene, qualifier, go_term
        from go_human 
        where gene_id in
        (select gene_id
        from disgenet
        where disease_name LIKE "Alzheimer's Disease" and EI >= 0.667 and num_pubs >= 11)
        and category = 'Process'
        group by go_id
        order by n_gene desc"""

# connect & show df (top 10)
df_go = pd.read_sql_query(q6, con)
df_go.head(10)


# ## Question 7
# - what other diseases these genes are associated with
#     - EI >= 0.667
#     - num_pub >= 11

# In[17]:


# write query
q7 = """select gene_symbol, num_pubs, EI, disease_name, count(gene_symbol) as n_alz
        from disgenet 
        where gene_symbol in (select gene_symbol
            from disgenet 
            where disease_name LIKE "Alzheimer's Disease"
            and EI >= 0.667 and num_pubs >= 11
            group by gene_symbol)
        and disease_type != 'group' and EI >= 0.667 and num_pubs >= 11
        group by disease_name
        order by n_alz desc
        limit 10"""

# connect & show df
df_other = pd.read_sql_query(q7, con)
df_other


# ## Question 8
# - visualize Alzheimer’s genes and the top-10 Alzheimer’s-related diseases as a graph using the NetworkX library

# In[18]:


# to be used later in query
# save question 4 query as a new table on dbeaver
t4 = """create table alz_gene as
        select gene_symbol, num_pubs, EI
        from disgenet 
        where disease_name LIKE "Alzheimer's Disease"
        and EI >= 0.667 and num_pubs >= 11
        group by gene_symbol
        order by num_pubs desc"""

# save question 7 query as a new table on dbeaver
t7 = """create table top_alz as
        select gene_symbol, num_pubs, EI, disease_name, count(gene_symbol) as n_alz
        from disgenet 
        where gene_symbol in (select gene_symbol
            from disgenet 
            where disease_name LIKE "Alzheimer's Disease"
            and EI >= 0.667 and num_pubs >= 11
            group by gene_symbol)
        and disease_type != 'group' and EI >= 0.667 and num_pubs >= 11
        group by disease_name
        order by n_alz desc
        limit 10"""


# In[23]:


# write query for alzhelmer's genes
q_8 = """select gene_symbol, num_pubs, disease_name
         from disgenet 
         where gene_symbol in (select gene_symbol from alz_gene)
         and disease_name in (select disease_name from top_alz) 
         order by num_pubs desc
         limit 200"""

# connect 
net = pd.read_sql_query(q_8, con)

# plot networkx & label the chart - given
plt.figure(figsize=(15,15), dpi=100)
G = nx.from_pandas_edgelist(net, 'gene_symbol', 'disease_name', 
                            create_using=nx.Graph()) 
nx.draw_networkx(G, with_labels=True, node_size=50)


# ## Research
# Question: Identify the top 300 genes with the highest number of total publications, and find the relationship between the DPI, DSI, and the number of publications of the gene.
# 
# Conclusion: Based on the scatterplot, the gene with the highest DPI and the lowest DSI has more publications than genes with the lowest DSI and DPI. Furthermore, the size of the plot is based on the number of unique diseases that is associated with each gene (scaled by 1/50). It demonstrated that a higher DPI would associate to more diseases related to the gene, which may correlate to an increase in the number of publications.
# 

# In[24]:


# write query
# n_disease = count of unique diseases associated with each gene
research_q = """select sum(num_pubs) as total_pub, gene_name, gene_symbol, disease_name, DSI, DPI, EI, count(distinct disease_name) as n_disease
            from disgenet 
            group by gene_symbol
            order by total_pub desc
            limit 300"""

# connect & show df
research = pd.read_sql_query(research_q, con)
research


# In[25]:


# plot a scatter plot
r_scat = plt.scatter(research.DPI, np.log10(research.total_pub), c=research.DSI, 
                   s=research.n_disease/50, alpha=0.6, cmap='viridis')
plt.text (0.65, 4.6, "note: markersize is based on num of disease per gene*(1/50)", fontsize=7)

# label the plots & add in legend
plt.xlabel('Disease Pleiotrophy Index (DPI)', fontsize=14)
plt.ylabel('Total Number of Publications', fontsize=14)
plt.colorbar(r_scat, label='Disease Specificity Index (DSI) ')
plt.title('DPI vs Number of Publications', fontsize=14)
plt.grid(alpha=0.4)
plt.show()


# In[ ]:




