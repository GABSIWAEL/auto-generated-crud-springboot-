import os
import uuid


# Function to enforce authorization and set the authorized MAC address


def generate_entity_class(package_name, class_name, fields):
    fields_code = ""
    for field in fields:
        fields_code += f"    private {field[1]} {field[0]};\n"

    entity_class = f"package {package_name}.Entity;\n\n"
    entity_class += "import jakarta.persistence.*;\n"
    entity_class += "import lombok.*;\n"
    entity_class += "import java.io.Serializable;\n"
    entity_class += "import java.util.Set;\n\n"
    entity_class += "@Entity\n"
    entity_class += "@Getter\n@Setter\n@AllArgsConstructor\n@NoArgsConstructor\n"
    entity_class += f"@Table(name=\"{class_name.lower()}\")\n\n"
    entity_class += f"public class {class_name} implements Serializable {{\n"
    entity_class += "    @Id\n"
    entity_class += "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    entity_class += "    @Column(name=\"id\")\n"
    entity_class += "    private Long id;\n\n"
    entity_class += fields_code + "\n"
   # Remove the @ManyToOne and @OneToMany annotations and related fields
    # entity_class += f"    @ManyToOne\n"
    # entity_class += f"    private Foyer foyer;\n\n"
    # entity_class += f"    @OneToMany(cascade = CascadeType.ALL, mappedBy = \"{class_name.lower()}\")\n"
    # entity_class += f"    private Set<Chambre> chambres;\n"
    entity_class += "}\n"

    return entity_class


def generate_controller_class(package_name, class_name):
    controller_class = f"package {package_name}.Controller;\n\n"
    controller_class += f"import {package_name}.Entity.{class_name};\n"
    controller_class += f"import {package_name}.Service.I{class_name}Service;\n"
    controller_class += "import io.swagger.v3.oas.annotations.Operation;\n"
    controller_class += "import io.swagger.v3.oas.annotations.tags.Tag;\n"
    controller_class += "import lombok.AllArgsConstructor;\n"
    controller_class += "import org.springframework.web.bind.annotation.*;\n"
    controller_class += "import java.util.List;\n\n"
    controller_class += f"@Tag(name = \"Gestion {class_name}\")\n"
    controller_class += "@RestController\n@AllArgsConstructor\n"
    controller_class += f"@RequestMapping(\"/{class_name.lower()}\")\n"
    controller_class += f"public class {class_name}RestController {{\n"
    controller_class += f"    I{class_name}Service {class_name.lower()}Service;\n\n"
    controller_class += f"    @Operation(description = \"recuperer toutes les {class_name.lower()} de la base de donnees\")\n"
    controller_class += f"    @GetMapping(\"/retrieve-all-{class_name.lower()}s\")\n"
    controller_class += f"    public List<{class_name}> get{class_name}s() {{\n"
    controller_class += f"        List<{class_name}> list{class_name}s = {class_name.lower()}Service.retrieveAll{class_name}s();\n"
    controller_class += f"        return list{class_name}s;\n    }}\n\n"
    controller_class += f"    @Operation(description = \"recuperer le {class_name.lower()} de la base de donnees\")\n"
    controller_class += f"    @GetMapping(\"/retrieve-{class_name.lower()}/{{{class_name.lower()}-id}}\")\n"
    controller_class += f"    public {class_name} retrieve{class_name}(@PathVariable(\"{class_name.lower()}-id\") Long {class_name.lower()}Id) {{\n"
    controller_class += f"        {class_name} {class_name.lower()} = {class_name.lower()}Service.retrieve{class_name}({class_name.lower()}Id);\n"
    controller_class += f"        return {class_name.lower()};\n    }}\n\n"
    controller_class += f"    @Operation(description = \"ajouter le {class_name.lower()} de la base de donnees\")\n"
    controller_class += f"    @PostMapping(\"/add-{class_name.lower()}\")\n"
    controller_class += f"    public {class_name} add{class_name}(@RequestBody {class_name} c) {{\n"
    controller_class += f"        {class_name} {class_name.lower()} = {class_name.lower()}Service.add{class_name}(c);\n"
    controller_class += f"        return {class_name.lower()};\n    }}\n\n"
    controller_class += f"    @Operation(description = \"suppprimer le {class_name.lower()} de la base de donnees\")\n"
    controller_class += f"    @DeleteMapping(\"/remove-{class_name.lower()}/{{{class_name.lower()}-id}}\")\n"
    controller_class += f"    public void remove{class_name}(@PathVariable(\"{class_name.lower()}-id\") Long {class_name.lower()}Id) {{\n"
    controller_class += f"        {class_name.lower()}Service.remove{class_name}({class_name.lower()}Id);\n    }}\n\n"
    controller_class += f"    @Operation(description = \"modifier le {class_name.lower()} de la base de donnees\")\n"
    controller_class += f"    @PutMapping(\"/modify-{class_name.lower()}\")\n"
    controller_class += f"    public {class_name} modify{class_name}(@RequestBody {class_name} c) {{\n"
    controller_class += f"        {class_name} {class_name.lower()} = {class_name.lower()}Service.modify{class_name}(c);\n"
    controller_class += f"        return {class_name.lower()};\n    }}\n}}"

    return controller_class


def generate_repository_interface(package_name, class_name):
    repository_interface = f"package {package_name}.Repository;\n\n"
    repository_interface += f"import {package_name}.Entity.{class_name};\n"
    repository_interface += "import org.springframework.data.jpa.repository.JpaRepository;\n"
    repository_interface += "import org.springframework.stereotype.Repository;\n\n"
    repository_interface += "@Repository\n"
    repository_interface += f"public interface {class_name}Repository extends JpaRepository<{class_name}, Long> {{\n}}"

    return repository_interface


def generate_service_interface(package_name, class_name):
    service_interface = f"package {package_name}.Service;\n\n"
    service_interface += f"import {package_name}.Entity.{class_name};\n"
    service_interface += "import java.util.List;\n\n"
    service_interface += f"public interface I{class_name}Service {{\n"
    service_interface += f"    public List<{class_name}> retrieveAll{class_name}s();\n"
    service_interface += f"    public {class_name} retrieve{class_name}(Long id);\n"
    service_interface += f"    public {class_name} add{class_name}({class_name} c);\n"
    service_interface += f"    public void remove{class_name}(Long id);\n"
    service_interface += f"    public {class_name} modify{class_name}({class_name} {class_name});\n}}"

    return service_interface


def generate_service_impl_class(package_name, class_name):
    service_impl_class = f"package {package_name}.ServiceImpl;\n\n"
    service_impl_class += f"import {package_name}.Entity.{class_name};\n"
    service_impl_class += f"import {package_name}.Repository.{class_name}Repository;\n"
    service_impl_class += f"import {package_name}.Service.I{class_name}Service;\n"
    service_impl_class += "import jakarta.persistence.EntityNotFoundException;\n"
    service_impl_class += "import lombok.AllArgsConstructor;\n"
    service_impl_class += "import org.springframework.stereotype.Service;\n"
    service_impl_class += "import java.util.List;\n"
    service_impl_class += "import java.util.Optional;\n\n"
    service_impl_class += "@Service\n"
    service_impl_class += "@AllArgsConstructor\n"
    service_impl_class += f"public class {class_name}ServiceImpl  implements I{class_name}Service {{\n"
    service_impl_class += f"    {class_name}Repository {class_name.lower()}Repository;\n"
    service_impl_class += f"    @Override\n"
    service_impl_class += f"    public List<{class_name}> retrieveAll{class_name}s() {{\n"
    service_impl_class += f"        return {class_name.lower()}Repository.findAll();\n    }}\n\n"
    service_impl_class += f"    @Override\n"
    service_impl_class += f"    public {class_name} retrieve{class_name}(Long id) {{\n"
    service_impl_class += f"        return {class_name.lower()}Repository.findById(id).orElseThrow(() -> new EntityNotFoundException(\"{class_name} not found with id: \" + id));\n    }}\n\n"
    service_impl_class += f"    @Override\n"
    service_impl_class += f"    public {class_name} add{class_name}({class_name} c) {{\n"
    service_impl_class += f"        return {class_name.lower()}Repository.save(c);\n    }}\n\n"
    service_impl_class += f"    @Override\n"
    service_impl_class += f"    public void remove{class_name}(Long id) {{\n"
    service_impl_class += f"        {class_name.lower()}Repository.deleteById(id);\n    }}\n\n"
    service_impl_class += f"    @Override\n"
    service_impl_class += f"    public {class_name} modify{class_name}({class_name} {class_name.lower()}) {{\n"
    service_impl_class += f"        Optional<{class_name}> existing{class_name} = {class_name.lower()}Repository.findById({class_name.lower()}.getId());\n"
    service_impl_class += f"        if (existing{class_name}.isPresent()) {{\n"
    service_impl_class += f"            return {class_name.lower()}Repository.save({class_name.lower()});\n"
    service_impl_class += f"        }} else {{\n"
    service_impl_class += f"            throw new EntityNotFoundException(\"{class_name} not found with id: \" + {class_name.lower()}.getId());\n"
    service_impl_class += f"        }}\n    }}\n}}"

    return service_impl_class


def save_code_to_file(file_path, code):
    with open(file_path, "w") as file:
        file.write(code)


# Example usage
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
project_folder = os.path.join(desktop_path, "GeneratedSpringBootProject")

# Create project folder if it doesn't exist
os.makedirs(project_folder, exist_ok=True)
default_package_name = "com.example.generated"
# Entities
entities = []
while True:
    class_name = input("Enter entity class name (or type 'done' to finish): ")
    if class_name.lower() == 'done':
        break

    fields = []
    while True:
        field_name = input("Enter field name (or type 'done' to finish): ")
        if field_name.lower() == 'done':
            break
        field_type = input("Enter field type: ")
        fields.append((field_name, field_type))

    entities.append((class_name, fields))

packages = ['entities', 'controllers',
            'repositories', 'services', 'serviceimpl']

for entity in entities:
    class_name, fields = entity
    # Create entity folder within the project folder
    entity_folder = os.path.join(project_folder, packages[0], class_name)
    os.makedirs(entity_folder, exist_ok=True)

    # Use the default package name if package_name is not provided
    package_name = f"{default_package_name}.{packages[0]}"

    # Generate code for each component
    entity_code = generate_entity_class(package_name, class_name, fields)
    save_code_to_file(os.path.join(
        entity_folder, f"{class_name}.java"), entity_code)

    # Generate code for controller
    controller_folder = os.path.join(project_folder, packages[1])
    os.makedirs(controller_folder, exist_ok=True)
    package_name = f"{default_package_name}.{packages[1]}"
    controller_code = generate_controller_class(package_name, class_name)
    save_code_to_file(os.path.join(controller_folder,
                      f"{class_name}RestController.java"), controller_code)

    # Generate code for repository
    repository_folder = os.path.join(project_folder, packages[2])
    os.makedirs(repository_folder, exist_ok=True)
    package_name = f"{default_package_name}.{packages[2]}"
    repository_code = generate_repository_interface(package_name, class_name)
    save_code_to_file(os.path.join(repository_folder,
                      f"{class_name}Repository.java"), repository_code)

    # Generate code for service interface
    service_folder = os.path.join(project_folder, packages[3])
    os.makedirs(service_folder, exist_ok=True)
    package_name = f"{default_package_name}.{packages[3]}"
    service_interface_code = generate_service_interface(
        package_name, class_name)
    save_code_to_file(os.path.join(
        service_folder, f"I{class_name}Service.java"), service_interface_code)

    # Generate code for service implementation
    service_impl_folder = os.path.join(project_folder, packages[4])
    os.makedirs(service_impl_folder, exist_ok=True)
    package_name = f"{default_package_name}.{packages[4]}"
    service_impl_code = generate_service_impl_class(package_name, class_name)
    save_code_to_file(os.path.join(service_impl_folder,
                      f"{class_name}ServiceImpl.java"), service_impl_code)

print("Code generation completed. Check the 'GeneratedSpringBootProject' folder on your desktop.")
