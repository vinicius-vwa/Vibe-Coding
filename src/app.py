from __future__ import annotations

import streamlit as st
from sqlalchemy import select

from src.database import SessionLocal, init_db
from src.models import (
    Category,
    Client,
    Organization,
    Owner,
    Reservation,
    Sale,
    User,
    Vehicle,
)

st.set_page_config(page_title="Vibe Coding", page_icon="🚗", layout="wide")

HERO_IMAGE = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=1200&q=80"
SIDEBAR_IMAGE = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=500&q=80"

st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: #0b1020;
            color: #e2e8f0;
        }
        .stApp {
            background: radial-gradient(circle at top, rgba(96, 165, 250, 0.18), transparent 35%), #0b1020;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }
        .main .block-container {
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
            padding: 1.5rem 1.5rem 2rem 1.5rem;
            box-shadow: 0 25px 45px rgba(15, 23, 42, 0.35);
        }
        h1, h2, h3, h4, p, span, div {
            color: #f8fafc;
        }
        .stSidebar {
            background: linear-gradient(180deg, #020817 0%, #111827 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.2);
        }
        .stSidebar .stRadio > div {
            gap: 0.55rem;
        }
        .stSidebar [data-baseweb="radio"] > div {
            padding: 0.55rem 0.8rem;
            border-radius: 0.8rem;
            background: rgba(148, 163, 184, 0.1);
            color: white;
            border: 1px solid rgba(148, 163, 184, 0.12);
        }
        .stSidebar .stRadio label {
            color: white;
            font-weight: 600;
        }
        .stButton > button {
            border: none;
            border-radius: 0.8rem;
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            color: white;
            font-weight: 700;
            padding: 0.7rem 1.25rem;
            transition: transform 0.15s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 20px rgba(96, 165, 250, 0.35);
        }
        div[data-testid="stForm"] {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 1rem 1rem 0.5rem;
            box-shadow: 0 16px 35px rgba(2, 6, 23, 0.35);
        }
        [data-testid="stMetricValue"] {
            font-size: 1.9rem;
            font-weight: 800;
            color: #f8fafc;
        }
        [data-testid="stMetricLabel"] {
            font-weight: 600;
            color: #cbd5e1;
        }
        .summary-box {
            border-radius: 1rem;
            padding: 0.9rem 1rem;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 118, 110, 0.8));
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.28);
        }
        .summary-box div, .summary-box p, .summary-box h3 {
            color: #f8fafc !important;
        }
        .stImage img {
            border-radius: 1rem;
            box-shadow: 0 20px 35px rgba(15, 23, 42, 0.35);
        }
        .stCaptionContainer {
            color: #cbd5e1 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()


def sidebar_menu() -> str:
    st.sidebar.title("Menu")
    st.sidebar.caption("Gestão de automóveis")
    return st.sidebar.radio(
        "Entidades",
        [
            "Organizações",
            "Categorias",
            "Veículos",
            "Proprietários",
            "Usuários",
            "Clientes",
            "Reservas",
            "Vendas",
        ],
    )


def render_summary_cards() -> None:
    db = SessionLocal()
    total_organizations = db.query(Organization).count()
    total_vehicles = db.query(Vehicle).count()
    total_users = db.query(User).count()
    total_sales = db.query(Sale).count()
    db.close()

    cols = st.columns(4)
    metrics = [
        ("Organizações", total_organizations, "🏢"),
        ("Veículos", total_vehicles, "🚗"),
        ("Usuários", total_users, "👤"),
        ("Vendas", total_sales, "💰"),
    ]

    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="summary-box">
                    <div style="font-size: 0.85rem; color:#64748b; margin-bottom: 0.3rem;">{icon} {label}</div>
                    <div style="font-size: 2rem; font-weight: 800; color:#0f172a;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def render_organization_page():
    st.title("Organizações")
    db = SessionLocal()

    with st.form("new_organization"):
        st.subheader("Nova organização")
        name = st.text_input("Nome")
        cnpj = st.text_input("CNPJ")
        address = st.text_input("Endereço")
        phone = st.text_input("Telefone")
        active = st.checkbox("Ativa", value=True)
        submitted = st.form_submit_button("Salvar")
        if submitted:
            db.add(Organization(name=name, cnpj=cnpj or None, address=address or None, phone=phone or None, active=active))
            db.commit()
            st.success("Organização salva com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Organization)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Organization, selected_id)
        with st.form("edit_organization"):
            st.write(f"Editando organização #{record.id}")
            name = st.text_input("Nome", value=record.name)
            cnpj = st.text_input("CNPJ", value=record.cnpj or "")
            address = st.text_input("Endereço", value=record.address or "")
            phone = st.text_input("Telefone", value=record.phone or "")
            active = st.checkbox("Ativa", value=record.active)
            update = st.form_submit_button("Atualizar")
            if update:
                record.name = name
                record.cnpj = cnpj or None
                record.address = address or None
                record.phone = phone or None
                record.active = active
                db.commit()
                st.success("Organização atualizada.")

        if st.button("Excluir organização selecionada"):
            db.delete(record)
            db.commit()
            st.success("Organização removida.")
    else:
        st.info("Nenhuma organização cadastrada.")

    db.close()


def render_category_page():
    st.title("Categorias")
    db = SessionLocal()

    with st.form("new_category"):
        st.subheader("Nova categoria")
        name = st.text_input("Nome")
        description = st.text_input("Descrição")
        active = st.checkbox("Ativa", value=True)
        submitted = st.form_submit_button("Salvar")
        if submitted:
            db.add(Category(name=name, description=description or None, active=active))
            db.commit()
            st.success("Categoria salva com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Category)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Category, selected_id)
        with st.form("edit_category"):
            st.write(f"Editando categoria #{record.id}")
            name = st.text_input("Nome", value=record.name)
            description = st.text_input("Descrição", value=record.description or "")
            active = st.checkbox("Ativa", value=record.active)
            update = st.form_submit_button("Atualizar")
            if update:
                record.name = name
                record.description = description or None
                record.active = active
                db.commit()
                st.success("Categoria atualizada.")

        if st.button("Excluir categoria selecionada"):
            db.delete(record)
            db.commit()
            st.success("Categoria removida.")
    else:
        st.info("Nenhuma categoria cadastrada.")

    db.close()


def render_vehicle_page():
    st.title("Veículos")
    db = SessionLocal()
    organizations = db.scalars(select(Organization)).all()
    owners = db.scalars(select(Owner)).all()
    categories = db.scalars(select(Category)).all()

    with st.form("new_vehicle"):
        st.subheader("Novo veículo")
        brand = st.text_input("Marca")
        model = st.text_input("Modelo")
        year_manufacture = st.number_input("Ano de fabricação", min_value=1900, max_value=2100, value=2024)
        year_model = st.number_input("Ano do modelo", min_value=1900, max_value=2100, value=2024)
        plate = st.text_input("Placa")
        chassis = st.text_input("Chassi")
        color = st.text_input("Cor")
        mileage = st.number_input("Quilometragem", min_value=0.0, value=0.0)
        fuel_type = st.text_input("Combustível")
        transmission = st.text_input("Transmissão")
        price = st.number_input("Preço", min_value=0.0, value=0.0)
        description = st.text_area("Descrição")
        condition = st.text_input("Condição")
        available = st.checkbox("Disponível para venda", value=True)
        active = st.checkbox("Ativo", value=True)
        organization = st.selectbox("Organização", organizations, format_func=lambda org: org.name if org else "") if organizations else st.empty()
        owner = st.selectbox("Proprietário", owners, format_func=lambda owner: owner.name if owner else "") if owners else st.empty()
        selected_categories = st.multiselect("Categorias", [category.name for category in categories])
        submitted = st.form_submit_button("Salvar")
        if submitted:
            if not organizations:
                st.warning("Cadastre uma organização antes de criar um veículo.")
            else:
                vehicle = Vehicle(
                    brand=brand,
                    model=model,
                    year_manufacture=int(year_manufacture),
                    year_model=int(year_model),
                    plate=plate or None,
                    chassis=chassis or None,
                    color=color or None,
                    mileage=float(mileage),
                    fuel_type=fuel_type,
                    transmission=transmission,
                    price=float(price),
                    description=description or None,
                    condition=condition or "novo",
                    available=available,
                    active=active,
                    organization_id=organization.id,
                    owner_id=owner.id if owners else None,
                )
                db.add(vehicle)
                db.flush()
                if categories:
                    selected_items = [cat for cat in categories if cat.name in selected_categories]
                    vehicle.categories = selected_items
                db.commit()
                st.success("Veículo salvo com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Vehicle)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Vehicle, selected_id)
        with st.form("edit_vehicle"):
            st.write(f"Editando veículo #{record.id}")
            record.brand = st.text_input("Marca", value=record.brand)
            record.model = st.text_input("Modelo", value=record.model)
            record.year_manufacture = st.number_input("Ano de fabricação", min_value=1900, max_value=2100, value=record.year_manufacture)
            record.year_model = st.number_input("Ano do modelo", min_value=1900, max_value=2100, value=record.year_model)
            record.plate = st.text_input("Placa", value=record.plate or "")
            record.chassis = st.text_input("Chassi", value=record.chassis or "")
            record.color = st.text_input("Cor", value=record.color or "")
            record.mileage = st.number_input("Quilometragem", min_value=0.0, value=record.mileage)
            record.fuel_type = st.text_input("Combustível", value=record.fuel_type)
            record.transmission = st.text_input("Transmissão", value=record.transmission)
            record.price = st.number_input("Preço", min_value=0.0, value=record.price)
            record.description = st.text_area("Descrição", value=record.description or "")
            record.condition = st.text_input("Condição", value=record.condition)
            record.available = st.checkbox("Disponível", value=record.available)
            record.active = st.checkbox("Ativo", value=record.active)
            update = st.form_submit_button("Atualizar")
            if update:
                db.commit()
                st.success("Veículo atualizado.")

        if st.button("Excluir veículo selecionado"):
            db.delete(record)
            db.commit()
            st.success("Veículo removido.")
    else:
        st.info("Nenhum veículo cadastrado.")

    db.close()


def render_owner_page():
    st.title("Proprietários")
    db = SessionLocal()

    with st.form("new_owner"):
        st.subheader("Novo proprietário")
        name = st.text_input("Nome")
        document = st.text_input("CPF/CNPJ")
        email = st.text_input("E-mail")
        phone = st.text_input("Telefone")
        address = st.text_input("Endereço")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            db.add(Owner(name=name, document=document or None, email=email or None, phone=phone or None, address=address or None))
            db.commit()
            st.success("Proprietário salvo com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Owner)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Owner, selected_id)
        with st.form("edit_owner"):
            st.write(f"Editando proprietário #{record.id}")
            record.name = st.text_input("Nome", value=record.name)
            record.document = st.text_input("CPF/CNPJ", value=record.document or "")
            record.email = st.text_input("E-mail", value=record.email or "")
            record.phone = st.text_input("Telefone", value=record.phone or "")
            record.address = st.text_input("Endereço", value=record.address or "")
            update = st.form_submit_button("Atualizar")
            if update:
                db.commit()
                st.success("Proprietário atualizado.")

        if st.button("Excluir proprietário selecionado"):
            db.delete(record)
            db.commit()
            st.success("Proprietário removido.")
    else:
        st.info("Nenhum proprietário cadastrado.")

    db.close()


def render_user_page():
    st.title("Usuários")
    db = SessionLocal()
    organizations = db.scalars(select(Organization)).all()

    with st.form("new_user"):
        st.subheader("Novo usuário")
        name = st.text_input("Nome")
        email = st.text_input("E-mail")
        phone = st.text_input("Telefone")
        profile = st.text_input("Perfil", value="operador")
        active = st.checkbox("Ativo", value=True)
        organization = st.selectbox("Organização", organizations, format_func=lambda org: org.name if org else "") if organizations else st.empty()
        submitted = st.form_submit_button("Salvar")
        if submitted:
            if not organizations:
                st.warning("Cadastre uma organização antes de criar um usuário.")
            else:
                db.add(User(name=name, email=email, phone=phone or None, profile=profile, active=active, organization_id=organization.id))
                db.commit()
                st.success("Usuário salvo com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(User)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(User, selected_id)
        with st.form("edit_user"):
            st.write(f"Editando usuário #{record.id}")
            record.name = st.text_input("Nome", value=record.name)
            record.email = st.text_input("E-mail", value=record.email)
            record.phone = st.text_input("Telefone", value=record.phone or "")
            record.profile = st.text_input("Perfil", value=record.profile)
            record.active = st.checkbox("Ativo", value=record.active)
            update = st.form_submit_button("Atualizar")
            if update:
                db.commit()
                st.success("Usuário atualizado.")

        if st.button("Excluir usuário selecionado"):
            db.delete(record)
            db.commit()
            st.success("Usuário removido.")
    else:
        st.info("Nenhum usuário cadastrado.")

    db.close()


def render_client_page():
    st.title("Clientes")
    db = SessionLocal()

    with st.form("new_client"):
        st.subheader("Novo cliente")
        name = st.text_input("Nome")
        document = st.text_input("CPF/CNPJ")
        email = st.text_input("E-mail")
        phone = st.text_input("Telefone")
        address = st.text_input("Endereço")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            db.add(Client(name=name, document=document or None, email=email, phone=phone or None, address=address or None))
            db.commit()
            st.success("Cliente salvo com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Client)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Client, selected_id)
        with st.form("edit_client"):
            st.write(f"Editando cliente #{record.id}")
            record.name = st.text_input("Nome", value=record.name)
            record.document = st.text_input("CPF/CNPJ", value=record.document or "")
            record.email = st.text_input("E-mail", value=record.email)
            record.phone = st.text_input("Telefone", value=record.phone or "")
            record.address = st.text_input("Endereço", value=record.address or "")
            update = st.form_submit_button("Atualizar")
            if update:
                db.commit()
                st.success("Cliente atualizado.")

        if st.button("Excluir cliente selecionado"):
            db.delete(record)
            db.commit()
            st.success("Cliente removido.")
    else:
        st.info("Nenhum cliente cadastrado.")

    db.close()


def render_reservation_page():
    st.title("Reservas")
    db = SessionLocal()
    vehicles = db.scalars(select(Vehicle)).all()
    users = db.scalars(select(User)).all()
    clients = db.scalars(select(Client)).all()
    organizations = db.scalars(select(Organization)).all()

    with st.form("new_reservation"):
        st.subheader("Nova reserva")
        vehicle = st.selectbox("Veículo", vehicles, format_func=lambda item: f"{item.brand} {item.model}" if item else "") if vehicles else st.empty()
        user = st.selectbox("Usuário", users, format_func=lambda item: item.name if item else "") if users else st.empty()
        client = st.selectbox("Cliente", clients, format_func=lambda item: item.name if item else "") if clients else st.empty()
        organization = st.selectbox("Organização", organizations, format_func=lambda item: item.name if item else "") if organizations else st.empty()
        status = st.text_input("Status", value="ativo")
        observation = st.text_area("Observação")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            if not vehicles or not users or not clients or not organizations:
                st.warning("Cadastre veículos, usuários, clientes e organizações antes de criar reservas.")
            else:
                db.add(
                    Reservation(
                        vehicle_id=vehicle.id,
                        user_id=user.id,
                        client_id=client.id,
                        organization_id=organization.id,
                        status=status,
                        observation=observation or None,
                    )
                )
                db.commit()
                st.success("Reserva salva com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Reservation)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Reservation, selected_id)
        with st.form("edit_reservation"):
            st.write(f"Editando reserva #{record.id}")
            record.status = st.text_input("Status", value=record.status)
            record.observation = st.text_area("Observação", value=record.observation or "")
            update = st.form_submit_button("Atualizar")
            if update:
                db.commit()
                st.success("Reserva atualizada.")

        if st.button("Excluir reserva selecionada"):
            db.delete(record)
            db.commit()
            st.success("Reserva removida.")
    else:
        st.info("Nenhuma reserva cadastrada.")

    db.close()


def render_sale_page():
    st.title("Vendas")
    db = SessionLocal()
    vehicles = db.scalars(select(Vehicle)).all()
    buyers = db.scalars(select(Client)).all()
    sellers = db.scalars(select(User)).all()
    organizations = db.scalars(select(Organization)).all()

    with st.form("new_sale"):
        st.subheader("Nova venda")
        vehicle = st.selectbox("Veículo", vehicles, format_func=lambda item: f"{item.brand} {item.model}" if item else "") if vehicles else st.empty()
        buyer = st.selectbox("Comprador", buyers, format_func=lambda item: item.name if item else "") if buyers else st.empty()
        seller = st.selectbox("Vendedor", sellers, format_func=lambda item: item.name if item else "") if sellers else st.empty()
        organization = st.selectbox("Organização", organizations, format_func=lambda item: item.name if item else "") if organizations else st.empty()
        final_price = st.number_input("Preço final", min_value=0.0, value=0.0)
        payment_method = st.text_input("Pagamento", value="dinheiro")
        status = st.text_input("Status", value="concluida")
        observation = st.text_area("Observação")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            if not vehicles or not buyers or not sellers or not organizations:
                st.warning("Cadastre veículos, clientes, usuários e organizações antes de registrar uma venda.")
            else:
                db.add(
                    Sale(
                        vehicle_id=vehicle.id,
                        buyer_id=buyer.id,
                        seller_id=seller.id,
                        organization_id=organization.id,
                        final_price=float(final_price),
                        payment_method=payment_method,
                        status=status,
                        observation=observation or None,
                    )
                )
                db.commit()
                st.success("Venda salva com sucesso!")

    st.subheader("Registros")
    records = db.scalars(select(Sale)).all()
    if records:
        selected_id = st.selectbox("Selecione para editar ou excluir", [r.id for r in records], format_func=lambda value: f"#{value}")
        record = db.get(Sale, selected_id)
        with st.form("edit_sale"):
            st.write(f"Editando venda #{record.id}")
            record.final_price = st.number_input("Preço final", min_value=0.0, value=record.final_price)
            record.payment_method = st.text_input("Pagamento", value=record.payment_method)
            record.status = st.text_input("Status", value=record.status)
            record.observation = st.text_area("Observação", value=record.observation or "")
            update = st.form_submit_button("Atualizar")
            if update:
                db.commit()
                st.success("Venda atualizada.")

        if st.button("Excluir venda selecionada"):
            db.delete(record)
            db.commit()
            st.success("Venda removida.")
    else:
        st.info("Nenhuma venda cadastrada.")

    db.close()


def main() -> None:
    st.sidebar.image(SIDEBAR_IMAGE, width=220)

    hero_col, info_col = st.columns([2.2, 1.1])
    with hero_col:
        st.image(HERO_IMAGE, width=900)
    with info_col:
        st.markdown(
            """
            <div class="summary-box" style="padding:1.2rem; margin-top:1rem;">
                <div style="font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.08em;">Painel principal</div>
                <h3 style="margin:0.5rem 0; color:#0f172a;">Gestão completa de automóveis</h3>
                <p style="margin:0; color:#475569; line-height:1.5;">
                    Cadastre veículos, clientes, reservas, vendas e controle o fluxo da sua revenda com rapidez.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.title("Sistema de Gestão de Automóveis")
    st.caption("Dashboard para gestão de veículos, clientes, reservas e vendas")
    render_summary_cards()
    st.markdown("<br>", unsafe_allow_html=True)
    page = sidebar_menu()

    if page == "Organizações":
        render_organization_page()
    elif page == "Categorias":
        render_category_page()
    elif page == "Veículos":
        render_vehicle_page()
    elif page == "Proprietários":
        render_owner_page()
    elif page == "Usuários":
        render_user_page()
    elif page == "Clientes":
        render_client_page()
    elif page == "Reservas":
        render_reservation_page()
    elif page == "Vendas":
        render_sale_page()


if __name__ == "__main__":
    main()
