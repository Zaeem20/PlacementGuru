import os, time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx
import textwrap
import matplotlib.patches as mpatches
from graphviz import Digraph

load_dotenv()
genai.configure(api_key = os.environ["GEMINI_API_KEY"])

def get_roadmap_from_gemini(role):
    # Define the prompt for Gemini to generate a role-specific roadmap
    prompt = (
        f"Please create a flowchart describing the steps involved in a career roadmap for someone aspiring to become a {role}. "
        f"List the stages as nodes and specify the relationships as edges between them."
    )             
    # Fetch the response from the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    # Process the response into a roadmap format
    # Assume the response is a structured list of stages and tasks
    
    roadmap_text = response.text.strip()
    return parse_roadmap(roadmap_text)

def create_graphviz_diagram(nodes, edges):
    graph = Digraph(format='fig')

    # Add nodes to the graph
    for node in nodes:
        graph.node(node)

    # Create edges between nodes
    for from_node, to_node in edges:
        graph.edge(from_node, to_node)

    return graph

def parse_roadmap(roadmap_text):
    lines = roadmap_text.split("\n")
    nodes = set()
    edges = []

    for line in lines:
        if "->" in line:
            parts = line.split("->")
            from_node = parts[0].strip()
            to_node = parts[1].strip()
            edges.append((from_node, to_node))
            nodes.add(from_node)
            nodes.add(to_node)

    return nodes, edges

# Function to create a Graphviz diagram from the roadmap
def create_graphviz_diagram(nodes, edges):
    graph = Digraph(format='png')

    # Add nodes to the graph
    for node in nodes:
        graph.node(node)

    # Create edges between nodes
    for from_node, to_node in edges:
        graph.edge(from_node, to_node)

    # Set the size of the graph
    graph.attr(size='50,50')  # Adjust this size as needed
    graph.attr('node', fontsize='20')  # Adjust node font size
    graph.attr('edge', fontsize='20')  # Adjust edge font size

    return graph

role = st.text_input("Enter role")
difficulty = st.selectbox("Diffculty",options=("Beginner","Intermediate","Advance"))
if st.button("Generate Roadmap"):
    nodes, edges = get_roadmap_from_gemini(role)

    # Display the roadmap in tree format using Graphviz
    if nodes and edges:
        st.write(f"**Roadmap for {role}**")
        
        # Create and display the Graphviz diagram
        diagram = create_graphviz_diagram(nodes, edges)
        st.graphviz_chart(diagram)
    else:
        st.error("No roadmap found. Please try again.")