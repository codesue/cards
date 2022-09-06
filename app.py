import logging
import streamlit as st

try:
  import model_card_toolkit as mct
except ModuleNotFoundError as e:
  logging.warning("Unable to import model_card_toolkit. Using placeholder_mct_lib instead.")
  import placeholder_mct_lib as mct


_NUM_REFERENCES = 3


try:
  toolkit = mct.ModelCardToolkit()
  mc = toolkit.scaffold_assets()
except AttributeError:
  mc = mct.ModelCard()

model_card_html = ""
model_card_json = ""

hide_menu_style = "<style> #MainMenu {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("Create a Model Card")
st.markdown(
  """
  Welcome! 👋

  This app allows you to create a model card using 
  [Model Card Toolkit](https://www.tensorflow.org/responsible_ai/model_card_toolkit/guide).
  Please fill out the form below. Your model card will be rendered as HTML and 
  its metadata will be output as JSON.
  """
)

with st.form("model_card_form"):
  st.markdown("**Model Details**")
  name = st.text_input("Name", help="The name of the model.")
  path = st.text_input("Path", help="The path where the model is stored.")
  overview = st.text_area("Overview", help="A description of the model card.")
  documentation = st.text_area("Documentation", help="A more thorough description of the model and its usage.")
  with st.expander("Owner"):
    st.caption("""The individual or team who owns the model.""")
    owner_name = st.text_input("Name", help="The name of the model owner.")
    owner_contact = st.text_input(
      "Contact",
      help="""The contact information for the model owner or owners. These could
      be individual email addresses, a team mailing list expressly, or a
      monitored feedback form.""")
  with st.expander("Version"):
    st.caption("The version of the model.")
    version_name = st.text_input("Name", help="The name of the version.")
    version_date = st.date_input("Date", help="The date this version was released.")
    version_diff = st.text_area("Diff", help="The changes from the previous version.")
  with st.expander("License"):
    st.caption("""The license information for the model. If the model is licensed
      for use by others, include the license type. If the model is not licensed
      for future use, you may state that here as well.""")
    license_identifier = st.text_input(
      "Identifier",
      help="""A standard SPDX license identifier (https://spdx.org/licenses/), or
      'proprietary' for an unlicensed Module.""")
    license_custom_text = st.text_area("Custom Text", help="The text of a custom license.")
  with st.expander("References"):
    st.caption("""Provide any additional links the reader may need. You can link
      to foundational research, technical documentation, or other materials that
      may be useful to your audience.""")
    references = []
    for n in range(_NUM_REFERENCES):
      references.append(st.text_input(f"Reference {n + 1}"))
  with st.expander("Citation"):
    st.caption("""THow should the model be cited? If the model is based on published
      academic research, cite the research.""")
    citation_style = st.text_input(
      "Style", help="The citation style, such as MLA, APA, Chicago, or IEEE.")
    citation_citation = st.text_area("Citation", help="The citation.")

  submitted = st.form_submit_button("Submit")

  if submitted:
    owners, licenses, citations = ([], [], [])
    if owner_name or owner_contact:
      owners.append(mct.Owner(owner_name, owner_contact))
    version=mct.Version(version_name, str(version_date), version_diff)
    if license_identifier or license_custom_text:
      licenses.append(mct.License(license_identifier, license_custom_text))
    refs = [mct.Reference(ref) for ref in references if ref]
    if citation_citation:
      citations.append(mct.Citation(citation_style, citation_citation))
    version=mct.Version(version_name, str(version_date), version_diff)
    mc.model_details = mct.ModelDetails(
      name=name,
      overview=overview,
      owners=owners,
      documentation=documentation,
      version=version,
      licenses=licenses,
      references=refs,
      path=path,
    )

    try:
      model_card_html = toolkit.export_format(mc)
    except NameError:
      notice = "Unable to render model card since Model Card Toolkit isn't installed."
      logging.warning(notice)
      model_card_html = f"<b>{notice}</b>"
    model_card_json = mc.to_json()

st.header("Here's your model card! ✨")

model_card_tab, json_tab = st.tabs(["Model Card", "JSON"])

with model_card_tab:
  if model_card_html:
    st.download_button(
      label="Download model card HTML",
      data=model_card_html,
      file_name="model_card.html",
      mime="text/html",
    )
    st.components.v1.html(model_card_html, height=500, scrolling=True)

with json_tab:
  if model_card_json:
    st.download_button(
      label="Download model card JSON",
      data=model_card_json,
      file_name="model_card.json",
      mime="application/json",
    )
    st.json(model_card_json)
